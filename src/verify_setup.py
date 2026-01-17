"""
Setup Verification Script for ICPE 2026 Shaved Ice Project

Verifies: dependencies, folder structure, custom modules, dbt setup
"""

import sys
from pathlib import Path

# Define project root relative to this script (src/verify_setup.py -> project_root)
PROJECT_ROOT = Path(__file__).parent.parent

def check_dependencies():
    """Verify all required packages are installed."""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('scipy', 'scipy'),
        ('matplotlib', 'matplotlib'),
        ('seaborn', 'seaborn'),
        ('statsmodels', 'statsmodels'),
        ('pyarrow', 'pyarrow'),
        ('duckdb', 'duckdb'),
        ('jupyter', 'jupyter'),
        ('tqdm', 'tqdm'),
        ('dbt', 'dbt.cli.main'),  # dbt-core
    ]
    
    missing = []
    for display_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"   ✅ {display_name}")
        except ImportError:
            print(f"   ❌ {display_name} - NOT INSTALLED")
            missing.append(display_name)
    
    if missing:
        print(f"\n⚠️  Missing: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        return False
    print("\n✅ All dependencies installed!")
    return True


def check_folders():
    """Verify folder structure exists."""
    print("\n📁 Checking folder structure...")
    
    required = [
        'data', 'data/raw', 'data/processed',
        'notebooks', 'src', 'figures', 'paper',
        'sql', 'sql/models', 'sql/models/staging',
        'sql/models/intermediate', 'sql/models/marts'
    ]
    
    all_exist = True
    for folder in required:
        if (PROJECT_ROOT / folder).exists():
            print(f"   ✅ {folder}/")
        else:
            print(f"   ❌ {folder}/ - MISSING")
            all_exist = False
    
    return all_exist


def check_dbt_setup():
    """Verify dbt configuration files exist."""
    print("\n🔧 Checking dbt setup...")
    
    dbt_files = [
        ('dbt_project.yml', 'dbt project configuration'),
        ('profiles.yml', 'DuckDB connection profile'),
        ('sql/models/staging/stg_shaved_ice.sql', 'Staging model'),
        ('sql/models/intermediate/int_daily_demand.sql', 'Intermediate model'),
        ('sql/models/marts/mart_forecast_input.sql', 'Mart model'),
        ('sql/models/schema.yml', 'Model documentation'),
    ]
    
    all_exist = True
    for filepath, description in dbt_files:
        if (PROJECT_ROOT / filepath).exists():
            print(f"   ✅ {filepath}")
        else:
            print(f"   ❌ {filepath} - MISSING ({description})")
            all_exist = False
    
    if all_exist:
        print("\n✅ dbt setup complete!")
    return all_exist


def check_python_modules():
    """Test importing custom modules."""
    print("\n🐍 Checking Python modules...")
    
    # Ensure src is in python path
    src_path = str(PROJECT_ROOT / 'src')
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    
    modules = ['data_loader', 'duckdb_loader', 'forecasting', 'plotting', 'utils']
    all_ok = True
    
    for module in modules:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError as e:
            print(f"   ❌ {module} - ERROR: {e}")
            all_ok = False
    
    return all_ok


def check_dataset():
    """Check if dataset has been downloaded."""
    print("\n📊 Checking dataset...")
    
    dataset_path = PROJECT_ROOT / 'data/raw/shavedice-dataset'
    if dataset_path.exists():
        print(f"   ✅ Dataset found at {dataset_path}")
        return True
    else:
        print("   ⚠️  Dataset not yet downloaded")
        print("   Run: cd data\\raw && git clone https://github.com/Snowflake-Labs/shavedice-dataset.git")
        return False


def main():
    """Run all verification checks."""
    print("=" * 60)
    print("ICPE 2026 Shaved Ice Project - Setup Verification")
    print("=" * 60)
    
    checks = [
        ("Dependencies", check_dependencies),
        ("Folder Structure", check_folders),
        ("dbt Setup", check_dbt_setup),
        ("Python Modules", check_python_modules),
        ("Dataset", check_dataset),
    ]
    
    results = []
    for name, func in checks:
        try:
            results.append((name, func()))
        except Exception as e:
            print(f"\n❌ {name} check failed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status:12} {name}")
    
    print("=" * 60)
    
    core_passed = all(r for n, r in results if n != "Dataset")
    
    if core_passed:
        print("\n🎉 Setup complete!")
        print("\nNext steps (run from project root):")
        print("1. cd data\\raw && git clone https://github.com/Snowflake-Labs/shavedice-dataset.git && cd ..\\..") 
        print("2. dbt run --profiles-dir .")
        print("3. jupyter notebook")
        return 0
    else:
        print("\n⚠️  Setup incomplete - fix issues above")
        return 1


if __name__ == "__main__":
    sys.exit(main())
