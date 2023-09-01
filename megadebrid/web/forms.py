from pathlib import Path

from wtforms.validators import regexp, DataRequired
from wtforms import Form, StringField, TextAreaField


class SaveFileForm(Form):
    url = StringField(
        "URL of the file to download",
        validators=[DataRequired()],
        render_kw={"class": "form-control mb-2"},
    )
    folder = StringField(
        "Folder to save the file",
        render_kw={"class": "form-control mb-2"},
        default=Path.home() / "Downloads",
    )


class DebridAndSaveFileForm(Form):
    link = StringField(
        "Link to unrestrict",
        validators=[DataRequired()],
        render_kw={"class": "form-control mb-2"},
    )
    folder = StringField(
        "Folder to save the file",
        render_kw={"class": "form-control mb-2"},
        default=Path.home() / "Downloads",
    )
    password = StringField(
        "Link password (optional)", render_kw={"class": "form-control mb-2"}, default=""
    )


class DownloadMagnetForm(Form):
    magnet = TextAreaField(
        "Magnet Link",
        validators=[DataRequired()],
        render_kw={"class": "form-control mb-2", "rows": "3"},
    )
    folder = StringField(
        "Folder to save the file",
        render_kw={"class": "form-control mb-2"},
        default=Path.home() / "Downloads",
    )


class DownloadTorrentForm(Form):
    torrent_path = StringField(
        "Torrent File Path",
        validators=[DataRequired(), regexp(".*\.torrent$")],
        render_kw={"class": "form-control mb-2"},
    )
    folder = StringField(
        "Folder to save the file",
        render_kw={"class": "form-control mb-2"},
        default=Path.home() / "Downloads",
    )
