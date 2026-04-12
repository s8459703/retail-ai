light_theme = """
/* ── Light Theme Overrides ───────────────────────────────── */
[data-theme="light"] body {
    background: linear-gradient(135deg, #f4f6fb 0%, #eaecf7 100%);
}
[data-theme="light"] .sidebar {
    box-shadow: 2px 0 20px rgba(99,102,241,0.08);
    border-right: 1px solid rgba(99,102,241,0.12);
}
[data-theme="light"] .nav-item { color: #3d3d6b; }
[data-theme="light"] .nav-item:hover,
[data-theme="light"] .nav-item.active { background: rgba(99,102,241,0.1); color: #1a1a2e; }
[data-theme="light"] .sidebar-footer { border-top: 1px solid rgba(99,102,241,0.12); }
[data-theme="light"] .stat-card {
    background: #ffffff;
    border: 1px solid rgba(99,102,241,0.12);
    box-shadow: 0 2px 12px rgba(99,102,241,0.06);
}
[data-theme="light"] .stat-card:hover {
    box-shadow: 0 8px 24px rgba(99,102,241,0.12);
    border-color: rgba(99,102,241,0.25);
}
[data-theme="light"] .chart-card,
[data-theme="light"] .table-card,
[data-theme="light"] .settings-card {
    background: #ffffff;
    border: 1px solid rgba(99,102,241,0.1);
    box-shadow: 0 2px 12px rgba(99,102,241,0.06);
}
[data-theme="light"] .topbar-user,
[data-theme="light"] .topbar-date {
    background: #ffffff;
    border: 1px solid rgba(99,102,241,0.12);
    color: #3d3d6b;
}
[data-theme="light"] thead th {
    background: #f8f9ff;
    color: #6b7280;
    border-bottom: 2px solid rgba(99,102,241,0.1);
}
[data-theme="light"] tbody td { color: #3d3d6b; border-bottom: 1px solid rgba(99,102,241,0.06); }
[data-theme="light"] tbody tr:hover td { background: rgba(99,102,241,0.04); color: #1a1a2e; }
[data-theme="light"] .category-badge {
    background: rgba(99,102,241,0.1);
    border-color: rgba(99,102,241,0.2);
    color: #6366f1;
}
[data-theme="light"] .table-count { background: #f4f6fb; border-color: rgba(99,102,241,0.12); color: #6b7280; }
[data-theme="light"] .welcome-banner {
    background: linear-gradient(135deg, rgba(99,102,241,0.08), rgba(139,92,246,0.05));
    border-color: rgba(99,102,241,0.2);
}
[data-theme="light"] .quick-action-card {
    background: #ffffff;
    border-color: rgba(99,102,241,0.1);
    box-shadow: 0 2px 8px rgba(99,102,241,0.05);
}
[data-theme="light"] .quick-action-card:hover { box-shadow: 0 8px 20px rgba(99,102,241,0.12); }
[data-theme="light"] .btn.secondary {
    background: #f4f6fb;
    color: #3d3d6b;
    border-color: rgba(99,102,241,0.2);
}
[data-theme="light"] .btn.secondary:hover {
    background: rgba(99,102,241,0.08);
    border-color: rgba(99,102,241,0.35);
    color: #1a1a2e;
}
[data-theme="light"] .settings-input {
    background: #f4f6fb;
    border-color: rgba(99,102,241,0.15);
    color: #1a1a2e;
}
[data-theme="light"] .settings-input::placeholder { color: #9ca3af; }
[data-theme="light"] .toggle-track { background: rgba(99,102,241,0.15); }
[data-theme="light"] .theme-btn { background: #f4f6fb; border-color: rgba(99,102,241,0.15); color: #6b7280; }
[data-theme="light"] .drop-zone { background: #f8f9ff; }
[data-theme="light"] .filter-select {
    background: #f4f6fb;
    border-color: rgba(99,102,241,0.15);
    color: #1a1a2e;
}
[data-theme="light"] .filter-select option { background: #ffffff; color: #1a1a2e; }
[data-theme="light"] ::-webkit-scrollbar-track { background: #f4f6fb; }
[data-theme="light"] ::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.25); }
[data-theme="light"] .page-header p { color: #3d3d6b; }
[data-theme="light"] .qa-desc { color: #6b7280; }
[data-theme="light"] .sidebar-footer .user-role { color: #6b7280; }
[data-theme="light"] .model-info-item {
    background: #f8f9ff;
    border-color: rgba(99,102,241,0.1);
}
[data-theme="light"] .plan-card {
    background: #ffffff;
    border-color: rgba(99,102,241,0.12);
    box-shadow: 0 2px 12px rgba(99,102,241,0.06);
}
[data-theme="light"] .plan-name,
[data-theme="light"] .plan-price { color: #1a1a2e; }
[data-theme="light"] .feat-yes { color: #3d3d6b; }
[data-theme="light"] .feat-no  { color: #9ca3af; }
[data-theme="light"] .settings-row { border-bottom-color: rgba(99,102,241,0.06); }
[data-theme="light"] .settings-card-header { border-bottom-color: rgba(99,102,241,0.1); }
[data-theme="light"] .settings-row-desc { color: #6b7280; }
[data-theme="light"] .upload-col-item { border-bottom-color: rgba(99,102,241,0.06); }
[data-theme="light"] .upload-col-name { color: #3d3d6b; }
[data-theme="light"] .upload-col-type { background: #f4f6fb; border-color: rgba(99,102,241,0.1); color: #6b7280; }
[data-theme="light"] .progress-bar { background: rgba(99,102,241,0.1); }
[data-theme="light"] .sidebar-toggle {
    background: rgba(99,102,241,0.1);
    border-color: rgba(99,102,241,0.2);
    color: #3d3d6b;
}
"""

content = open('static/css/dashboard.css', encoding='utf-8').read()
if '[data-theme="light"] body' not in content:
    content += light_theme
    open('static/css/dashboard.css', 'w', encoding='utf-8').write(content)
    print("Light theme overrides added.")
else:
    # Replace existing light theme overrides
    start = content.find('/* \u2500\u2500 Light Theme Overrides')
    if start != -1:
        content = content[:start] + light_theme
        open('static/css/dashboard.css', 'w', encoding='utf-8').write(content)
        print("Light theme overrides replaced.")
    else:
        print("Already has light theme but no marker found.")
