import enum

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse


class TestVariables(enum.Enum):
    USERNAME = 'Test_User'
    NEW_USERNAME = 'New_User'
    GROUP_POST_SLAG = 'test-slug'
    INDEX = reverse('posts:index')
    GROUP_POST = reverse('posts:group_posts',
                         args=[GROUP_POST_SLAG]
                         )
    PROFILE = reverse('posts:profile',
                      args=[USERNAME]
                      )
    NEW_PROFILE = reverse('posts:profile',
                          args=[NEW_USERNAME]
                          )
    FOLLOW_USER = reverse('posts:profile_follow',
                          args=[NEW_USERNAME]
                          )
    UNFOLLOW_USER = reverse('posts:profile_unfollow',
                            args=[NEW_USERNAME]
                            )
    FOLLOW_INDEX = reverse('posts:follow_index')
    CREATE_POST = reverse('posts:post_create')
    AUTH = reverse('users:login')
    SIGNUP = reverse('users:signup')
    FAKE_PAGE = '/fake_page/'
    templates_url_names = {
        INDEX: 'posts/index.html',
        GROUP_POST: 'posts/group_list.html',
        PROFILE: 'posts/profile.html',
        CREATE_POST: 'posts/create_post.html',
        FOLLOW_INDEX: 'posts/follow.html',
        FAKE_PAGE: 'core/404.html'
    }
    small_gif = (
        b'\x47\x49\x46\x38\x39\x61\x02\x00'
        b'\x01\x00\x80\x00\x00\x00\x00\x00'
        b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
        b'\x00\x00\x00\x2C\x00\x00\x00\x00'
        b'\x02\x00\x01\x00\x00\x02\x02\x0C'
        b'\x0A\x00\x3B'
    )
    uploaded = SimpleUploadedFile(
        name='small.gif',
        content=small_gif,
        content_type='image/gif'
    )
