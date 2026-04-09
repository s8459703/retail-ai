import os
import json
import hashlib
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, redirect, session, url_for
from flask_dance.contrib.google import make_google_blueprint, google
from sklearn.linear_model import LinearRegression

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

# Google OAuth — set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in environment
os.environ.setdefault("OAUTHLIB_INSECURE_TRANSPORT", "1")  # allow http in dev
google_bp = make_google_blueprint(
    client_id=os.environ.get("GOOGLE_CLIENT_ID", ""),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET", ""),
    scope=["openid", "https://www.googleapis.com/auth/userinfo.email",
           "https://www.googleapis.com/auth/userinfo.profile"],
    redirect_to="google_login_callback",
)
app.register_blueprint(google_bp, url_prefix="/google_auth")

DEFAULT_DATA_PATH = os.path.join(os.path.dirname(__file__), "dataset", "retail_sales.csv")
UPLOAD_FOLDER    = os.path.join(os.path.dirname(__file__), "dataset", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

REQUIRED_COLUMNS = {"Total Amount", "Category", "Year", "Month"}

ADMIN_USER  = os.environ.get("ADMIN_USER", "admin")
ADMIN_PASS  = os.environ.get("ADMIN_PASS", "changeme")
USERS_FILE  = os.path.join(os.path.dirname(__file__), "dataset", "users.json")


def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()


def load_users():
    if not os.path.exists(USERS_FILE):
        # Seed with admin account
        users = {ADMIN_USER: {"password": hash_password(ADMIN_PASS), "role": "admin"}}
        save_users(users)
        return users
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def verify_user(username, password):
    users = load_users()
    user  = users.get(username)
    if not user:
        return False
    # Support both hashed and legacy plain-text (admin env var)
    return user["password"] == hash_password(password)


def get_data_path():
    try:
        return session.get("data_path", DEFAULT_DATA_PATH)
    except RuntimeError:
        return DEFAULT_DATA_PATH


def load_data():
    df = pd.read_csv(get_data_path())
    df.columns = df.columns.str.strip()
    return df


def is_logged_in():
    return "user" in session


def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_logged_in():
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


@app.route("/")  # public: landing page
def home():
    return render_template("index.html")


@app.route("/home")
@login_required
def home_inner():
    return render_template("home.html")


@app.route("/welcome")  # public: pre-login welcome page
def welcome():
    return render_template("welcome.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if is_logged_in():
        return redirect(url_for("dashboard"))
    error = None
    success = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm  = request.form.get("confirm_password", "")

        if not username or not password:
            error = "Username and password are required."
        elif len(username) < 3:
            error = "Username must be at least 3 characters."
        elif len(password) < 6:
            error = "Password must be at least 6 characters."
        elif password != confirm:
            error = "Passwords do not match."
        else:
            users = load_users()
            if username in users:
                error = "Username already exists. Please choose another."
            else:
                users[username] = {"password": hash_password(password), "role": "user"}
                save_users(users)
                success = "Account created! You can now sign in."
    return render_template("register.html", error=error, success=success)


@app.route("/login", methods=["GET", "POST"])
def login():
    if is_logged_in():
        return redirect(url_for("dashboard"))

    error = None
    if request.method == "POST":
        user = request.form.get("username", "").strip()
        pwd = request.form.get("password", "")

        if verify_user(user, pwd):
            session["user"] = user
            return redirect(url_for("dashboard"))
        error = "Invalid username or password."

    return render_template("login.html", error=error)


@app.route("/logout")  # public: must be accessible to clear expired sessions
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/google_login_callback")
def google_login_callback():
    if not google.authorized:
        return redirect(url_for("google.login"))
    try:
        resp = google.get("/oauth2/v2/userinfo")
        if not resp.ok:
            return redirect(url_for("login"))
        info     = resp.json()
        email    = info.get("email", "")
        name     = info.get("name", email.split("@")[0])
        username = email.split("@")[0]
        # Auto-register Google user if not exists
        users = load_users()
        if username not in users:
            users[username] = {"password": "", "role": "user", "email": email, "google": True}
            save_users(users)
        session["user"] = username
        return redirect(url_for("dashboard"))
    except Exception:
        return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    try:
        df = load_data()
    except Exception as e:
        return render_template("error.html", message=f"Failed to load data: {e}"), 500

    # Summary stats
    total_sales  = round(float(df["Total Amount"].sum()), 2)
    total_orders = len(df)
    avg_sales    = round(float(df["Total Amount"].mean()), 2)
    best_product = df.groupby("Category")["Total Amount"].sum().idxmax()

    # Category breakdown
    cat_group   = df.groupby("Category")["Total Amount"]
    categories  = cat_group.sum().index.tolist()
    cat_sales   = [round(float(v), 2) for v in cat_group.sum().values]
    cat_counts  = df.groupby("Category").size().reindex(categories).tolist()
    cat_avgs    = [round(float(v), 2) for v in cat_group.mean().reindex(categories).values]

    table_rows = [
        {"category": c, "total": t, "count": n, "avg": a}
        for c, t, n, a in zip(categories, cat_sales, cat_counts, cat_avgs)
    ]

    # Monthly trend
    df["YearMonth"] = df["Year"].astype(str) + "-" + df["Month"].astype(str).str.zfill(2)
    monthly = df.groupby("YearMonth")["Total Amount"].sum().sort_index()
    monthly_labels = monthly.index.tolist()
    monthly_sales  = [round(float(v), 2) for v in monthly.values]

    # Gender breakdown
    gender_counts = df["Gender"].value_counts()
    gender_labels = gender_counts.index.tolist()
    gender_values = gender_counts.values.tolist()

    # City breakdown
    city_group  = df.groupby("Place")["Total Amount"].sum().sort_values(ascending=False)
    city_labels = city_group.index.tolist()
    city_sales  = [round(float(v), 2) for v in city_group.values]

    # Extra stats
    max_sale = round(float(df["Total Amount"].max()), 2)
    min_sale = round(float(df["Total Amount"].min()), 2)
    avg_age  = round(float(df["Age"].mean()), 1) if "Age" in df.columns else "—"

    # Brand breakdown
    brand_group  = df.groupby("Brand")["Total Amount"].sum().sort_values(ascending=False).head(10)
    brand_labels = brand_group.index.tolist()
    brand_sales  = [round(float(v), 2) for v in brand_group.values]

    return render_template(
        "dashboard.html",
        total_sales=total_sales,
        total_orders=total_orders,
        avg_sales=avg_sales,
        best_product=best_product,
        max_sale=max_sale,
        min_sale=min_sale,
        avg_age=avg_age,
        categories=categories,
        category_sales=cat_sales,
        table_rows=table_rows,
        monthly_labels=monthly_labels,
        monthly_sales=monthly_sales,
        gender_labels=gender_labels,
        gender_values=gender_values,
        city_labels=city_labels,
        city_sales=city_sales,
        brand_labels=brand_labels,
        brand_sales=brand_sales,
    )


@app.route("/predict", methods=["GET", "POST"])
@login_required
def predict():
    prediction = None
    error = None

    try:
        df = load_data()
        df["YearMonth"] = df["Year"].astype(str) + "-" + df["Month"].astype(str).str.zfill(2)
        monthly = df.groupby("YearMonth")["Total Amount"].sum().sort_index()
        monthly_labels = monthly.index.tolist()
        monthly_sales  = [round(float(v), 2) for v in monthly.values]
    except Exception:
        monthly_labels, monthly_sales = [], []

    if request.method == "POST":
        try:
            df = load_data()
            df["Index"] = np.arange(len(df))
            model = LinearRegression()
            model.fit(df[["Index"]], df["Total Amount"])
            prediction = round(float(model.predict(pd.DataFrame([[len(df)]], columns=["Index"]))[0]), 2)
        except Exception as e:
            error = f"Prediction failed: {e}"

    return render_template(
        "predict.html",
        prediction=prediction,
        error=error,
        monthly_labels=monthly_labels,
        monthly_sales=monthly_sales,
    )


@app.route("/future")
@login_required
def future():
    STEPS = session.get("forecast_steps", 10)
    try:
        df = load_data()
        df["Index"] = np.arange(len(df))

        model = LinearRegression()
        model.fit(df[["Index"]], df["Total Amount"])

        # Last 30 transactions as history context
        history_df     = df.tail(30)
        history_labels = [f"T-{len(df) - i}" for i in history_df["Index"].tolist()]
        history_values = [round(float(v), 2) for v in history_df["Total Amount"].tolist()]

        # Next STEPS predictions
        next_indices   = np.arange(len(df), len(df) + STEPS).reshape(-1, 1)
        raw_preds      = model.predict(next_indices)
        forecast_values = [round(float(v), 2) for v in raw_preds]
        forecast_labels = [f"T+{i + 1}" for i in range(STEPS)]

    except Exception as e:
        return render_template("error.html", message=f"Forecast failed: {e}"), 500

    return render_template(
        "future.html",
        forecast_steps=STEPS,
        forecast_labels=forecast_labels,
        forecast_values=forecast_values,
        forecast_rows=list(zip(forecast_labels, forecast_values)),
        forecast_total=round(sum(forecast_values), 2),
        forecast_avg=round(sum(forecast_values) / STEPS, 2),
        forecast_max=round(max(forecast_values), 2),
        forecast_min=round(min(forecast_values), 2),
        history_labels=history_labels,
        history_values=history_values,
    )


@app.route("/premium")
@login_required
def premium():
    return render_template("premium.html")


@app.route("/category/<category>")
@login_required
def category(category):
    try:
        df = load_data()
        valid = df["Category"].unique().tolist()
        if category not in valid:
            return render_template("error.html", message=f"Category '{category}' not found."), 404

        filtered = df[df["Category"] == category]

        total_sales  = round(float(filtered["Total Amount"].sum()), 2)
        total_orders = len(filtered)
        avg_order    = round(float(filtered["Total Amount"].mean()), 2)
        max_order    = round(float(filtered["Total Amount"].max()), 2)
        min_order    = round(float(filtered["Total Amount"].min()), 2)

        # Brand breakdown for this category
        brand_group  = filtered.groupby("Brand")["Total Amount"].sum().sort_values(ascending=False)
        brand_labels = brand_group.index.tolist()
        brand_sales  = [round(float(v), 2) for v in brand_group.values]

        # Sub category breakdown
        sub_group  = filtered.groupby("Sub Category")["Total Amount"].sum().sort_values(ascending=False)
        sub_labels = sub_group.index.tolist()
        sub_sales  = [round(float(v), 2) for v in sub_group.values]

        # City breakdown for this category
        city_group  = filtered.groupby("Place")["Total Amount"].sum().sort_values(ascending=False)
        city_labels = city_group.index.tolist()
        city_sales  = [round(float(v), 2) for v in city_group.values]

        # Gender breakdown
        gender_counts = filtered["Gender"].value_counts()
        gender_labels = gender_counts.index.tolist()
        gender_values = gender_counts.values.tolist()

        # Monthly trend
        filtered = filtered.copy()
        filtered["YearMonth"] = filtered["Year"].astype(str) + "-" + filtered["Month"].astype(str).str.zfill(2)
        monthly = filtered.groupby("YearMonth")["Total Amount"].sum().sort_index()

        # Recent transactions
        recent = df[df["Category"] == category].tail(20)[
            ["Transaction Id", "Day", "Month", "Year", "Place", "Gender", "Age", "Brand", "Sub Category", "Quantity", "Price Per Unit", "Total Amount"]
        ].to_dict(orient="records")

    except Exception as e:
        return render_template("error.html", message=f"Failed to load category: {e}"), 500

    return render_template(
        "category.html",
        category=category,
        total_sales=total_sales,
        total_orders=total_orders,
        avg_order=avg_order,
        max_order=max_order,
        min_order=min_order,
        city_labels=city_labels,
        city_sales=city_sales,
        brand_labels=brand_labels,
        brand_sales=brand_sales,
        sub_labels=sub_labels,
        sub_sales=sub_sales,
        gender_labels=gender_labels,
        gender_values=gender_values,
        monthly_labels=monthly.index.tolist(),
        monthly_sales=[round(float(v), 2) for v in monthly.values],
        recent=recent,
        all_categories=valid,
    )


@app.route("/filter")
@login_required
def filter_view():
    try:
        df = load_data()
        # Get filter params
        sel_category = request.args.get("category", "All")
        sel_sub      = request.args.get("sub_category", "All")
        sel_brand    = request.args.get("brand", "All")
        sel_city     = request.args.get("city", "All")
        sel_gender   = request.args.get("gender", "All")

        # All options for dropdowns
        all_categories = sorted(df["Category"].unique().tolist())
        all_cities     = sorted(df["Place"].unique().tolist())
        all_genders    = sorted(df["Gender"].unique().tolist())

        # Apply filters
        fdf = df.copy()
        if sel_category != "All":
            fdf = fdf[fdf["Category"] == sel_category]
        all_subs   = sorted(fdf["Sub Category"].unique().tolist())
        all_brands = sorted(fdf["Brand"].unique().tolist())
        if sel_sub != "All":
            fdf = fdf[fdf["Sub Category"] == sel_sub]
        if sel_brand != "All":
            fdf = fdf[fdf["Brand"] == sel_brand]
        if sel_city != "All":
            fdf = fdf[fdf["Place"] == sel_city]
        if sel_gender != "All":
            fdf = fdf[fdf["Gender"] == sel_gender]

        total_sales  = round(float(fdf["Total Amount"].sum()), 2) if len(fdf) else 0
        total_orders = len(fdf)
        avg_order    = round(float(fdf["Total Amount"].mean()), 2) if len(fdf) else 0
        total_brands = fdf["Brand"].nunique() if len(fdf) else 0

        # Charts
        cat_group    = fdf.groupby("Category")["Total Amount"].sum().sort_values(ascending=False)
        brand_group  = fdf.groupby("Brand")["Total Amount"].sum().sort_values(ascending=False).head(10)
        city_group   = fdf.groupby("Place")["Total Amount"].sum().sort_values(ascending=False)
        gender_group = fdf["Gender"].value_counts()
        sub_group    = fdf.groupby("Sub Category")["Total Amount"].sum().sort_values(ascending=False)

        fdf2 = fdf.copy()
        fdf2["YearMonth"] = fdf2["Year"].astype(str) + "-" + fdf2["Month"].astype(str).str.zfill(2)
        monthly = fdf2.groupby("YearMonth")["Total Amount"].sum().sort_index()

        # Table
        cols = ["Transaction Id", "Day", "Month", "Year", "Place", "Gender",
                "Age", "Category", "Sub Category", "Brand", "Quantity", "Price Per Unit", "Total Amount"]
        table_rows = fdf[cols].head(50).to_dict(orient="records")

    except Exception as e:
        return render_template("error.html", message=f"Filter failed: {e}"), 500

    return render_template(
        "filter.html",
        sel_category=sel_category, sel_sub=sel_sub, sel_brand=sel_brand,
        sel_city=sel_city, sel_gender=sel_gender,
        all_categories=all_categories, all_subs=all_subs, all_brands=all_brands,
        all_cities=all_cities, all_genders=all_genders,
        total_sales=total_sales, total_orders=total_orders,
        avg_order=avg_order, total_brands=total_brands,
        cat_labels=cat_group.index.tolist(),
        cat_sales=[round(float(v), 2) for v in cat_group.values],
        brand_labels=brand_group.index.tolist(),
        brand_sales=[round(float(v), 2) for v in brand_group.values],
        city_labels=city_group.index.tolist(),
        city_sales=[round(float(v), 2) for v in city_group.values],
        gender_labels=gender_group.index.tolist(),
        gender_values=gender_group.values.tolist(),
        sub_labels=sub_group.index.tolist(),
        sub_sales=[round(float(v), 2) for v in sub_group.values],
        monthly_labels=monthly.index.tolist(),
        monthly_sales=[round(float(v), 2) for v in monthly.values],
        table_rows=table_rows,
    )


@app.route("/categories")
@login_required
def categories():
    try:
        df = load_data()
        cat_stats = []
        for cat in sorted(df["Category"].unique()):
            cdf = df[df["Category"] == cat]
            cat_stats.append({
                "name":       cat,
                "total":      round(float(cdf["Total Amount"].sum()), 2),
                "count":      len(cdf),
                "avg":        round(float(cdf["Total Amount"].mean()), 2),
                "brands":     cdf["Brand"].nunique(),
                "sub_cats":   sorted(cdf["Sub Category"].unique().tolist()),
            })
    except Exception as e:
        return render_template("error.html", message=f"Failed: {e}"), 500
    return render_template("categories.html", cat_stats=cat_stats)


@app.route("/subcategory/<category>/<subcategory>")
@login_required
def subcategory(category, subcategory):
    try:
        df  = load_data()
        fdf = df[(df["Category"] == category) & (df["Sub Category"] == subcategory)].copy()
        if fdf.empty:
            return render_template("error.html", message=f"No data for {category} / {subcategory}."), 404

        all_brands = sorted(fdf["Brand"].unique().tolist())
        sel_brand  = request.args.get("brand", "All")
        search     = request.args.get("search", "").strip()

        if sel_brand != "All":
            fdf = fdf[fdf["Brand"] == sel_brand]
        if search:
            mask = (
                fdf["Brand"].str.contains(search, case=False, na=False) |
                fdf["Product Name"].str.contains(search, case=False, na=False) |
                fdf["Variant"].str.contains(search, case=False, na=False)
            )
            fdf = fdf[mask]

        total_products = len(fdf)
        total_revenue  = round(float(fdf["Total Amount"].sum()), 2) if total_products else 0
        avg_price      = round(float(fdf["Price Per Unit"].mean()), 2) if total_products else 0
        max_price      = round(float(fdf["Price Per Unit"].max()), 2) if total_products else 0
        min_price      = round(float(fdf["Price Per Unit"].min()), 2) if total_products else 0
        top_brand      = fdf.groupby("Brand")["Total Amount"].sum().idxmax() if total_products else "—"

        brand_group  = fdf.groupby("Brand")["Total Amount"].sum().sort_values(ascending=False)
        brand_labels = brand_group.index.tolist()
        brand_sales  = [round(float(v), 2) for v in brand_group.values]
        brand_counts = fdf.groupby("Brand").size().reindex(brand_labels).tolist()
        brand_rows   = list(zip(brand_labels, brand_sales, brand_counts))

        bins   = [0, 500, 1000, 2000, 3000, 5000, 99999]
        labels = ["<500", "500-1K", "1K-2K", "2K-3K", "3K-5K", "5K+"]
        fdf["PriceBucket"] = pd.cut(fdf["Price Per Unit"], bins=bins, labels=labels)
        price_dist = fdf["PriceBucket"].value_counts().reindex(labels, fill_value=0)

        city_group = fdf.groupby("Place")["Total Amount"].sum().sort_values(ascending=False)
        gender_cnt = fdf["Gender"].value_counts()

        products = fdf[["Transaction Id", "Brand", "Product Name", "Variant",
                        "Price Per Unit", "Quantity", "Total Amount", "Place", "Gender"]]\
                     .sort_values("Total Amount", ascending=False).head(50)\
                     .to_dict(orient="records")

        all_subs = sorted(df[df["Category"] == category]["Sub Category"].unique().tolist())

    except Exception as e:
        return render_template("error.html", message=f"Failed: {e}"), 500

    return render_template(
        "analysis.html",
        category=category, subcategory=subcategory,
        sel_brand=sel_brand, all_brands=all_brands, search=search,
        total_products=total_products, total_revenue=total_revenue,
        avg_price=avg_price, max_price=max_price, min_price=min_price,
        top_brand=top_brand,
        brand_labels=brand_labels, brand_sales=brand_sales,
        brand_counts=brand_counts, brand_rows=brand_rows,
        price_labels=labels, price_counts=price_dist.tolist(),
        city_labels=city_group.index.tolist(),
        city_sales=[round(float(v), 2) for v in city_group.values],
        gender_labels=gender_cnt.index.tolist(),
        gender_values=gender_cnt.values.tolist(),
        products=products,
        all_subs=all_subs,
    )


@app.route("/subcategory/<category>/<subcategory>/export")
@login_required
def subcategory_export(category, subcategory):
    try:
        from flask import Response
        import io
        df  = load_data()
        fdf = df[(df["Category"] == category) & (df["Sub Category"] == subcategory)].copy()
        sel_brand = request.args.get("brand", "All")
        search    = request.args.get("search", "").strip()
        if sel_brand != "All":
            fdf = fdf[fdf["Brand"] == sel_brand]
        if search:
            mask = (
                fdf["Brand"].str.contains(search, case=False, na=False) |
                fdf["Product Name"].str.contains(search, case=False, na=False) |
                fdf["Variant"].str.contains(search, case=False, na=False)
            )
            fdf = fdf[mask]
        buf = io.StringIO()
        fdf.to_csv(buf, index=False)
        fname = f"{category}_{subcategory}_{sel_brand}.csv".replace(" ", "_")
        return Response(buf.getvalue(), mimetype="text/csv",
                        headers={"Content-Disposition": f"attachment; filename={fname}"})
    except Exception as e:
        return render_template("error.html", message=f"Export failed: {e}"), 500


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    error = None
    success = None
    preview_rows = []
    preview_cols = []
    file_info = None

    if request.method == "POST":
        file = request.files.get("datafile")

        if not file or file.filename == "":
            error = "No file selected. Please choose a CSV file."
        elif not file.filename.lower().endswith(".csv"):
            error = "Invalid file type. Only .csv files are accepted."
        else:
            try:
                df = pd.read_csv(file)
                df.columns = df.columns.str.strip()

                missing = REQUIRED_COLUMNS - set(df.columns)
                if missing:
                    error = f"Missing required columns: {', '.join(sorted(missing))}"
                elif len(df) == 0:
                    error = "The uploaded file is empty."
                else:
                    # Save file
                    safe_name = "uploaded_" + session["user"] + ".csv"
                    save_path = os.path.join(UPLOAD_FOLDER, safe_name)
                    df.to_csv(save_path, index=False)
                    session["data_path"] = save_path

                    # Build preview
                    preview_cols = df.columns.tolist()
                    preview_rows = df.head(10).values.tolist()
                    file_info = {
                        "name": file.filename,
                        "rows": len(df),
                        "cols": len(df.columns),
                        "total": round(float(df["Total Amount"].sum()), 2) if "Total Amount" in df.columns else None,
                    }
                    success = f"File uploaded successfully — {len(df):,} rows loaded. Dashboard now uses your data."
            except Exception as e:
                error = f"Failed to read file: {e}"

    return render_template(
        "upload.html",
        error=error,
        success=success,
        preview_cols=preview_cols,
        preview_rows=preview_rows,
        file_info=file_info,
        using_custom=session.get("data_path") != DEFAULT_DATA_PATH and "data_path" in session,
    )


@app.route("/upload/reset")
@login_required
def upload_reset():
    session.pop("data_path", None)
    return redirect(url_for("upload"))


@app.route("/profile")
@login_required
def profile():
    try:
        df = load_data()
        total_orders     = len(df)
        total_sales      = round(float(df["Total Amount"].sum()), 2)
        total_categories = df["Category"].nunique()
        best_product     = df.groupby("Category")["Total Amount"].sum().idxmax()
    except Exception:
        total_orders, total_sales, total_categories, best_product = 0, 0.0, 0, "—"

    return render_template(
        "profile.html",
        total_orders=total_orders,
        total_sales=total_sales,
        total_categories=total_categories,
        best_product=best_product,
    )


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    success = None
    error   = None
    if request.method == "POST":
        action = request.form.get("action")
        if action == "change_password":
            current = request.form.get("current_password", "")
            new_pwd = request.form.get("new_password", "")
            confirm = request.form.get("confirm_password", "")
            if not verify_user(session["user"], current):
                error = "Current password is incorrect."
            elif len(new_pwd) < 6:
                error = "New password must be at least 6 characters."
            elif new_pwd != confirm:
                error = "New passwords do not match."
            else:
                users = load_users()
                users[session["user"]]["password"] = hash_password(new_pwd)
                save_users(users)
                success = "Password updated successfully."
        elif action == "save_forecast_steps":
            steps = request.form.get("forecast_steps", "10")
            if steps in ("10", "20", "30"):
                session["forecast_steps"] = int(steps)
                success = f"Forecast steps set to {steps}."
    return render_template(
        "settings.html",
        success=success,
        error=error,
        forecast_steps=session.get("forecast_steps", 10),
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
