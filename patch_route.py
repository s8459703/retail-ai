content = open('app.py', encoding='utf-8').read()

old = '''@app.route("/subcategory/<category>/<subcategory>")
@login_required
def subcategory(category, subcategory):
    try:
        df   = load_data()
        fdf  = df[(df["Category"] == category) & (df["Sub Category"] == subcategory)]
        if fdf.empty:
            return render_template("error.html", message=f"No data for {category} / {subcategory}."), 404

        total_products = len(fdf)
        total_revenue  = round(float(fdf["Total Amount"].sum()), 2)
        avg_price      = round(float(fdf["Price Per Unit"].mean()), 2)
        max_price      = round(float(fdf["Price Per Unit"].max()), 2)
        min_price      = round(float(fdf["Price Per Unit"].min()), 2)
        top_brand      = fdf.groupby("Brand")["Total Amount"].sum().idxmax()

        brand_group  = fdf.groupby("Brand")["Total Amount"].sum().sort_values(ascending=False)
        brand_labels = brand_group.index.tolist()
        brand_sales  = [round(float(v), 2) for v in brand_group.values]
        brand_counts = fdf.groupby("Brand").size().reindex(brand_labels).tolist()

        # Price distribution buckets
        bins   = [0, 500, 1000, 2000, 3000, 5000, 99999]
        labels = ["<500", "500-1K", "1K-2K", "2K-3K", "3K-5K", "5K+"]
        fdf2   = fdf.copy()
        fdf2["PriceBucket"] = pd.cut(fdf2["Price Per Unit"], bins=bins, labels=labels)
        price_dist = fdf2["PriceBucket"].value_counts().reindex(labels, fill_value=0)

        city_group  = fdf.groupby("Place")["Total Amount"].sum().sort_values(ascending=False)
        gender_cnt  = fdf["Gender"].value_counts()

        products = fdf[["Transaction Id", "Brand", "Product Name", "Variant",
                        "Price Per Unit", "Quantity", "Total Amount", "Place", "Gender"]]\\
                     .sort_values("Total Amount", ascending=False).head(50)\\
                     .to_dict(orient="records")

        brand_rows = list(zip(brand_labels, brand_sales, brand_counts))

        all_subs = sorted(df[df["Category"] == category]["Sub Category"].unique().tolist())

    except Exception as e:
        return render_template("error.html", message=f"Failed: {e}"), 500

    return render_template(
        "analysis.html",
        category=category, subcategory=subcategory,
        total_products=total_products, total_revenue=total_revenue,
        avg_price=avg_price, max_price=max_price, min_price=min_price,
        top_brand=top_brand,
        brand_labels=brand_labels, brand_sales=brand_sales, brand_counts=brand_counts,
        brand_rows=brand_rows,
        price_labels=labels, price_counts=price_dist.tolist(),
        city_labels=city_group.index.tolist(),
        city_sales=[round(float(v), 2) for v in city_group.values],
        gender_labels=gender_cnt.index.tolist(),
        gender_values=gender_cnt.values.tolist(),
        products=products,
        all_subs=all_subs,
    )'''

new = '''@app.route("/subcategory/<category>/<subcategory>")
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
                        "Price Per Unit", "Quantity", "Total Amount", "Place", "Gender"]]\\
                     .sort_values("Total Amount", ascending=False).head(50)\\
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
        return render_template("error.html", message=f"Export failed: {e}"), 500'''

if old in content:
    content = content.replace(old, new)
    open('app.py', 'w', encoding='utf-8').write(content)
    print("SUCCESS: route updated")
else:
    print("ERROR: old text not found")
    # Try to find partial match
    idx = content.find('@app.route("/subcategory/<category>/<subcategory>")')
    print(f"Route found at index: {idx}")
