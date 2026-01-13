"""
Setup Verification Script for ICPE 2026 Shaved Ice Project

This script verifies that:
1. All required dependencies are installed correctly
2. Project folder structure exists
3. Custom modules can be imported
4. Basic functionality works

Run this after completing the initial setup.
"""

import sys
from pathlib import Path


def check_dependencies():
    """Verify all required packages are installed."""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        'pandas',
        'numpy',
        'scipy',
        'matplotlib',
        'seaborn',
        'statsmodels',
        'pyarrow',
        'duckdb',
        'jupyter',
        'ipykernel',
        'tqdm',
        'dateutil'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - NOT INSTALLED")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("   Run: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All dependencies installed correctly!")
        return True


def check_folder_structure():
    """Verify the project folder structure exists."""
    print("\n📁 Checking folder structure...")
    
    required_folders = [
        'data',
        'data/raw',
        'data/processed',
        'notebooks',
        'src',
        'figures',
        'paper',
        'paper/sections',
        'sql'
    ]
    
    all_exist = True
    
    for folder in required_folders:
        folder_path = Path(folder)
        if folder_path.exists():
            print(f"   ✅ {folder}/")
        else:
            print(f"   ❌ {folder}/ - MISSING")
            all_exist = False
    
    if all_exist:
        print("\n✅ All folders exist!")
    else:
        print("\n⚠️  Some folders are missing")
    
    return all_exist


def check_custom_modules():
    """Test importing custom modules."""
    print("\n🐍 Checking custom modules...")
    
    # Add src to path
    sys.path.insert(0, str(Path('src').absolute()))
    
    modules_to_test = [
        'data_loader',
        'forecasting',
        'plotting',
        'utils'
    ]
    
    all_imported = True
    
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError as e:
            print(f"   ❌ {module} - ERROR: {e}")
            all_imported = False
    
    if all_imported:
        print("\n✅ All custom modules import successfully!")
    else:
        print("\n⚠️  Some modules failed to import")
    
    return all_imported


def test_basic_functionality():
    """Test basic functionality of custom modules."""
    print("\n🔬 Testing basic functionality...")
    
    try:
        import pandas as pd
        import numpy as np
        from data_loader import validate_time_range
        from utils import add_time_features
        
        # Create test data
        dates = pd.date_range('2024-01-01', periods=100, freq='H')
        test_df = pd.DataFrame({
            'timestamp': dates,
            'demand': np.random.randint(10, 100, size=100)
        })
        
        # Test time features
        test_df_enhanced = add_time_features(test_df)
        assert 'hour' in test_df_enhanced.columns, "Time features not added"
        print("   ✅ Time feature engineering works")
        
        # Test validation
        validation = validate_time_range(test_df, timestamp_col='timestamp')
        assert validation['completeness'] == 100.0, "Validation failed"
        print("   ✅ Time range validation works")
        
        print("\n✅ Basic functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Functionality test failed: {e}")
        return False


def check_files():
    """Verify key files exist."""
    print("\n📄 Checking key files...")
    
    required_files = [
        'README.md',
        'requirements.txt',
        '.gitignore',
        'lab_notebook.md',
        'data/README.md',
        'figures/README.md',
        'src/__init__.py',
        'src/data_loader.py',
        'src/forecasting.py',
        'src/plotting.py',
        'src/utils.py',
        'notebooks/01_data_exploration.ipynb'
    ]
    
    all_exist = True
    
    for file in required_files:
        file_path = Path(file)
        if file_path.exists():
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - MISSING")
            all_exist = False
    
    if all_exist:
        print("\n✅ All key files exist!")
    else:
        print("\n⚠️  Some files are missing")
    
    return all_exist


def main():
    """Run all verification checks."""
    print("=" * 60)
    print("ICPE 2026 Shaved Ice Project - Setup Verification")
    print("=" * 60)
    
    checks = [
        ("Dependencies", check_dependencies),
        ("Folder Structure", check_folder_structure),
        ("Key Files", check_files),
        ("Custom Modules", check_custom_modules),
        ("Basic Functionality", test_basic_functionality)
    ]
    
    results = []
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"\n❌ {check_name} check failed with error: {e}")
            results.append((check_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:12} {check_name}")
    
    all_passed = all(result for _, result in results)
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 Setup complete - ready to analyze Shaved Ice data!")
        print("\nNext steps:")
        print("1. Download dataset: cd data/raw && git clone https://github.com/Snowflake-Labs/shavedice-dataset.git")
        print("2. Open Jupyter: jupyter notebook notebooks/01_data_exploration.ipynb")
        print("3. Start exploring the data!")
        return 0
    else:
        print("\n⚠️  Setup incomplete - please fix the issues above")
        return 1


if __name__ == "__main__":
    sys.exit(main())
