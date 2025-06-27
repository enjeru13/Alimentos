def require_admin(rol: str):
    """
    Lanza PermissionError si el rol dado no es 'admin'.
    """
    if rol != "admin":
        raise PermissionError("Permisos insuficientes. Se requiere rol 'admin'.")
