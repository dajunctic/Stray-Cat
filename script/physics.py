def is_collision_left(rect1, rect2):
    return rect1.right > rect2.left > rect1.left


def is_collision_right(rect1, rect2):
    return rect1.left < rect2.right < rect1.right


def is_collision_top(rect1, rect2):
    return rect1.bottom > rect2.top > rect1.top


def is_collision_bottom(rect1, rect2):
    return rect1.top < rect2.bottom < rect1.bottom
