from cloudinary_storage.storage import MediaCloudinaryStorage
import cloudinary
import cloudinary.api
import cloudinary.uploader
import os


RESOURCE_TYPES = {
    'IMAGE': 'image',
    'RAW': 'raw',
    'VIDEO': 'video'
}


class CustomStorage(MediaCloudinaryStorage):
    def _upload(self, name, content):
        options = {
            'use_filename': True,
            'resource_type': self._get_resource_type(name),
            'tags': self.TAG,
            'width': 400,
            'height': 400,
            'crop': 'scale',
            'quality': 'auto',
            'fetch_format': 'jpg',
            'secure': True,




        }
        folder = os.path.dirname(name)
        if folder:
            options['folder'] = folder
        return cloudinary.uploader.upload(content, **options)
