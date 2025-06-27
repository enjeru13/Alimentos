def require_admin(rol: str):

    if rol != "admin":
        raise PermissionError("Permisos insuficientes. Se requiere rol 'admin'.")
