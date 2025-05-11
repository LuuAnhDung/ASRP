import click
from flask.cli import FlaskGroup
from asrp import create_app
from asrp.extensions import db
from asrp.models import *  # import tất cả models của bạn

def create_my_app():
    """Factory function cho Flask CLI, trả về Flask app."""
    return create_app()

@click.group(cls=FlaskGroup, create_app=create_my_app)
def cli():
    """Management script cho ứng dụng ASRP."""
    pass

@cli.command("create-db")
def create_db():
    """Tạo cơ sở dữ liệu (tables)."""
    db.create_all()
    click.echo("✅ Cơ sở dữ liệu đã được tạo.")

if __name__ == "__main__":
    cli()
