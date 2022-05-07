import enum

from django.urls import reverse


class TestVariables(enum.Enum):
    USERNAME = 'Test_User'
    NEW_USERNAME = 'New_User'
    GROUP_POST_SLAG = 'test-slug'
    INDEX = reverse('posts:index')
    GROUP_POST = reverse('posts:group_posts',
                         kwargs={'slug': GROUP_POST_SLAG}
                         )
    PROFILE = reverse('posts:profile',
                      kwargs={'username': USERNAME}
                      )
    NEW_PROFILE = reverse('posts:profile',
                          kwargs={'username': NEW_USERNAME}
                          )
    FOLLOW_USER = reverse('posts:profile_follow',
                          kwargs={'username': NEW_USERNAME}
                          )
    UNFOLLOW_USER = reverse('posts:profile_unfollow',
                            kwargs={'username': NEW_USERNAME}
                            )
    FOLLOW_INDEX = reverse('posts:follow_index')
    CREATE_POST = reverse('posts:post_create')
    AUTH = reverse('users:login')
    SIGNUP = reverse('users:signup')
    FAKE_PAGE = '/fake_page/'
