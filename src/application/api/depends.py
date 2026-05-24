from application.domain.user.use_cases.get_user_by_id import GetUserByIdUseCase
from application.domain.user.use_cases.get_user_by_login import GetUserByLoginUseCase
from application.domain.user.use_cases.get_user_by_email import GetUserByEmailUseCase
from application.domain.user.use_cases.create_user import CreateUserUseCase
from application.domain.user.use_cases.delete_user import DeleteUserUseCase
from application.domain.user.use_cases.update_user import UpdateUserUseCase

from application.domain.post.use_cases.get_all_posts import GetAllPostsUseCase
from application.domain.post.use_cases.get_post_by_id import GetPostByIdUseCase
from application.domain.post.use_cases.create_post import CreatePostUseCase
from application.domain.post.use_cases.delete_post import DeletePostUseCase
from application.domain.post.use_cases.update_post import UpdatePostUseCase
from application.domain.post.use_cases.get_posts_by_author import GetPostsByAuthorUseCase
from application.domain.post.use_cases.add_post_image import AddPostImageUseCase
from application.domain.post.use_cases.get_post_images import GetPostImagesUseCase

from application.domain.comment.use_cases.get_comments_by_post import GetCommentsByPostUseCase
from application.domain.comment.use_cases.get_comment_by_id import GetCommentByIdUseCase
from application.domain.comment.use_cases.create_comment import CreateCommentUseCase
from application.domain.comment.use_cases.delete_comment import DeleteCommentUseCase
from application.domain.comment.use_cases.update_comment import UpdateCommentUseCase
from application.domain.comment.use_cases.add_comment_image import AddCommentImageUseCase
from application.domain.comment.use_cases.get_comment_images import GetCommentImagesUseCase

from application.domain.location.use_cases.get_all_locations import GetAllLocationsUseCase
from application.domain.location.use_cases.get_location_by_id import GetLocationByIdUseCase
from application.domain.location.use_cases.get_location_by_name import GetLocationByNameUseCase
from application.domain.location.use_cases.create_location import CreateLocationUseCase
from application.domain.location.use_cases.delete_location import DeleteLocationUseCase

from application.domain.category.use_cases.get_all_categories import GetAllCategoriesUseCase
from application.domain.category.use_cases.get_category_by_id import GetCategoryByIdUseCase
from application.domain.category.use_cases.get_category_by_slug import GetCategoryBySlugUseCase
from application.domain.category.use_cases.get_category_by_title import GetCategoryByTitleUseCase
from application.domain.category.use_cases.create_category import CreateCategoryUseCase
from application.domain.category.use_cases.delete_category import DeleteCategoryUseCase

from application.domain.auth.use_cases.authenticate_user import AuthenticateUserUseCase
from application.domain.auth.use_cases.create_access_token import CreateAccessTokenUseCase


def get_user_by_id_use_case() -> GetUserByIdUseCase:
    return GetUserByIdUseCase()

def get_user_by_login_use_case() -> GetUserByLoginUseCase:
    return GetUserByLoginUseCase()

def get_user_by_email_use_case() -> GetUserByEmailUseCase:
    return GetUserByEmailUseCase()

def create_user_use_case() -> CreateUserUseCase:
    return CreateUserUseCase()

def delete_user_use_case() -> DeleteUserUseCase:
    return DeleteUserUseCase()

def update_user_use_case() -> UpdateUserUseCase:
    return UpdateUserUseCase()


def get_posts_by_author_use_case() -> GetPostsByAuthorUseCase:
    return GetPostsByAuthorUseCase()

def get_all_posts_use_case() -> GetAllPostsUseCase:
    return GetAllPostsUseCase()

def get_post_by_id_use_case() -> GetPostByIdUseCase:
    return GetPostByIdUseCase()

def create_post_use_case() -> CreatePostUseCase:
    return CreatePostUseCase()

def delete_post_use_case() -> DeletePostUseCase:
    return DeletePostUseCase()

def update_post_use_case() -> UpdatePostUseCase:
    return UpdatePostUseCase()

def add_post_image_use_case() -> AddPostImageUseCase:
    return AddPostImageUseCase()

def get_post_images_use_case() -> GetPostImagesUseCase:
    return GetPostImagesUseCase()


def get_comments_by_post_use_case() -> GetCommentsByPostUseCase:
    return GetCommentsByPostUseCase()

def get_comment_by_id_use_case() -> GetCommentByIdUseCase:
    return GetCommentByIdUseCase()

def create_comment_use_case() -> CreateCommentUseCase:
    return CreateCommentUseCase()

def delete_comment_use_case() -> DeleteCommentUseCase:
    return DeleteCommentUseCase()

def update_comment_use_case() -> UpdateCommentUseCase:
    return UpdateCommentUseCase()

def add_comment_image_use_case() -> AddCommentImageUseCase:
    return AddCommentImageUseCase()

def get_comment_images_use_case() -> GetCommentImagesUseCase:
    return GetCommentImagesUseCase()


def get_all_locations_use_case() -> GetAllLocationsUseCase:
    return GetAllLocationsUseCase()

def get_location_by_id_use_case() -> GetLocationByIdUseCase:
    return GetLocationByIdUseCase()

def get_location_by_name_use_case() -> GetLocationByNameUseCase:
    return GetLocationByNameUseCase()

def create_location_use_case() -> CreateLocationUseCase:
    return CreateLocationUseCase()

def delete_location_use_case() -> DeleteLocationUseCase:
    return DeleteLocationUseCase()


def get_all_categories_use_case() -> GetAllCategoriesUseCase:
    return GetAllCategoriesUseCase()

def get_category_by_id_use_case() -> GetCategoryByIdUseCase:
    return GetCategoryByIdUseCase()

def get_category_by_slug_use_case() -> GetCategoryBySlugUseCase:
    return GetCategoryBySlugUseCase()

def get_category_by_title_use_case() -> GetCategoryByTitleUseCase:
    return GetCategoryByTitleUseCase()

def create_category_use_case() -> CreateCategoryUseCase:
    return CreateCategoryUseCase()

def delete_category_use_case() -> DeleteCategoryUseCase:
    return DeleteCategoryUseCase()

def authenticate_user_use_case() -> AuthenticateUserUseCase:
    return AuthenticateUserUseCase()

def create_access_token_use_case() -> CreateAccessTokenUseCase:
    return CreateAccessTokenUseCase()
