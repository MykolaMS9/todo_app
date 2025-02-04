from .models import UserSettings


def set_cards_per_page(user, cards_per_page):
    """
    Sets the number of Todo items per page for a specific user.

    This function updates the `cards_per_page` value in the `UserSettings` model
    for the given user. It modifies the number of items to display per page
    in the Todo list for that user.

    Args:
        user (User): The user whose settings need to be updated.
        cards_per_page (int): The number of Todo items to display per page.

    Side Effects:
        - Updates the `cards_per_page` value for the specified user in the `UserSettings` table.
    """
    UserSettings.objects.filter(user=user).update(cards_per_page=cards_per_page)
