from ..models import Cliente

def get_clientes():
    clientes = Cliente.objects.all()
    return clientes

def create_cliente_from_form(form_data):
    try:
        # nuevo_cliente = Cliente.objects.create(
        #     nombre=form_data['nombre'],
        #     apellido=form_data['apellido'],
        #     usuario=form_data['usuario'],
        #     correo=form_data['correo'],
        #     telefono=form_data['telefono'],
        # )
        # nuevo_cliente.save()
        # return nuevo_cliente

        cliente = {
            "nombre": form_data['nombre'],
            "apellido": form_data['apellido'],
            'usuario' : form_data['usuario'],
            'correo': form_data['correo'],
            'telefono': form_data['telefono'],
        }

        return cliente

        
    except Exception as e:
        # Aquí puedes manejar los errores de validación o lo que sea necesario
        # Esto es solo un ejemplo, en un proyecto real, deberías manejar esto con más detalle.
        return None