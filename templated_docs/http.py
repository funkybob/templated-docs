# --coding: utf8--

import os
import mimetypes

from django.http import FileResponse as BaseFileResponse


class DeleteOnClose:
    def __init__(self, filename):
        self.filename = filename

    def close(self):
        os.unlink(self.filename)


class FileResponse(BaseFileResponse):
    """
    One-time HTTP response with a generated file. DELETES A FILE AFTERWARDS!
    """
    def __init__(self, actual_file, visible_name, delete=True, *args, **kwargs):
        kwargs.setdefault('content_type', mimetypes.guess_type(actual_file)[0])
        super(FileResponse, self).__init__(open(actual_file, 'rb'), *args, **kwargs)
        self['Content-disposition'] = 'attachment; filename=%s' % visible_name
        if delete:
            self._closable_objects.append(DeleteOnClose(actual_file))
