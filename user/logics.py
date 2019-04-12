from swiper import settings
import os

def upload_avatar_to_server(uid,avatar):
    file_name = "avatar-%s" % uid + os.path.splitext(avatar.name)[1]
    save_path = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, file_name)

    with open(save_path, "wb") as fp:
        for chunk in avatar.chunks():
            fp.write(chunk)