"""
utils/db_seeder.py — Database Seeder
Creates default admin account if not exists.
"""

def seed_admin():
    try:
        from models.models import db, User
        from flask_bcrypt import Bcrypt
        
        bcrypt = Bcrypt()
        
        admin = User.query.filter_by(email='admin@mce.ac.in').first()
        if not admin:
            hashed = bcrypt.generate_password_hash('Admin@MCE2024').decode('utf-8')
            admin = User(
                name='T&P Admin',
                email='admin@mce.ac.in',
                password_hash=hashed,
                role='admin',
                branch='Administration',
                batch=2024
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Default admin created: admin@mce.ac.in / Admin@MCE2024")
        else:
            print("ℹ️ Admin already exists.")
    except Exception as e:
        print(f"⚠️ Seeder skipped: {e}")