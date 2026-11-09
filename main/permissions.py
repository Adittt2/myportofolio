from rest_framework.permissions import BasePermission, SAFE_METHODS

EDITOR_GROUP = "Editor"


def is_editor(user):
    """True bila akun sudah login dan anggota grup Editor."""
    return bool(
        user and user.is_authenticated
        and user.groups.filter(name=EDITOR_GROUP).exists()
    )


class IsPortfolioOwnerOrReadOnly(BasePermission):
    message = "Only the portfolio owner can change certifications."

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_superuser
        )


class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    """
    Pengunjung & pengguna biasa : baca saja
    Editor                      : baca + PUT/PATCH
    Pemilik (superuser)         : semua method
    """

    message = "Hanya pemilik portofolio atau Editor yang dapat mengubah pengalaman."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        return request.method in ("PUT", "PATCH") and is_editor(user)