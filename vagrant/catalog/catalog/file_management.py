"""File management functions for managing user uploaded image files."""
import os

from catalog import app


def allowed_file(filename):
    """Check if the filename has one of the allowed extensions.

    Args:
        filename (str): Name of file to check.
    """
    return ('.' in filename and filename.rsplit('.', 1)[1] in
            app.config['ALLOWED_EXTENSIONS'])


def delete_image(filename):
    """Delete an item image file from the filesystem.

    Args:
        filename (str): Name of file to be deleted.
    """
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    except OSError:
        print "Error deleting image file %s" % filename
