#Fix Terminal errors

## File "/workspace/flask-sqlalchemy-task-manager/taskmanager/__init__.py", line 3

The error message you're encountering indicates that the `flask_sqlalchemy` package is trying to import a function or module (`_app_ctx_stack`) that no longer exists in the version of Flask you're using.

The function `_app_ctx_stack` has been deprecated in recent versions of Flask. To resolve this issue, you have a couple of options:

### Option 1: Update `flask_sqlalchemy`
Make sure you have the latest version of `Flask-SQLAlchemy`, as newer versions have likely removed or updated this deprecated import. You can update it by running:

```bash
pip install --upgrade Flask-SQLAlchemy
```

### Option 2: Use an Older Version of Flask
Alternatively, you can use an older version of Flask that still supports `_app_ctx_stack`. You can install Flask version 1.1.x (where this functionality was still present):

```bash
pip install Flask==1.1.4
```

### Option 3: Modify the Code (Not Recommended)
If you're comfortable modifying the code, you could try replacing the deprecated import in `flask_sqlalchemy` (though this may introduce other issues down the line). It's better to stick with one of the options above.


## ImportError: cannot import name 'escape' from 'jinja2' (/workspace/.pip-modules/lib/python3.12/site-packages/jinja2/__init__.py)

The error you're seeing indicates that the `escape` function has been removed or relocated in the version of `Jinja2` you're using. This likely occurred due to changes in `Jinja2` in newer versions.

### Solution: Upgrade Flask or Jinja2

#### Option 1: Update Flask
Newer versions of Flask have adapted to the changes in `Jinja2`, so updating Flask may resolve the issue:

```bash
pip install --upgrade Flask
```

#### Option 2: Downgrade Jinja2
If upgrading Flask doesn't work or you're not ready to update Flask, you can downgrade `Jinja2` to a version where the `escape` function is still available. For example, you can downgrade to Jinja2 version 3.0.3:

```bash
pip install Jinja2==3.0.3
```

### Option 3: Modify Code (Temporary)
If you're modifying the codebase directly, you can replace `escape` with `MarkupSafe.escape` (as this function was moved to the `MarkupSafe` library). In your Flask-related files, find any instance of `escape` and replace it with:

```python
from markupsafe import escape
```
