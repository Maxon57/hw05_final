import enum

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
