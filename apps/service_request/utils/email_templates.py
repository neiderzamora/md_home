from django.template.loader import render_to_string

def service_request_accepted_email(doctor, patient, service_request_id):
    """
    Generates email components for an accepted service request.

    :param doctor: DoctorUser object accepting the request.
    :param patient: PatientUser object receiving the notification.
    :return: Dictionary with 'subject', 'message', 'sender', and 'recipients'.
    """
    subject = 'Solicitud de Servicio Aceptada'
    message = (
        f'Hola {patient.first_name},\n\n'
        f'El doctor {doctor.first_name} {doctor.last_name} ha aceptado tu solicitud de servicio y está en camino.\n\n'
        'El servicio llegara en un rango de una a tres horas.\n\n'
        f'Para consultar el estado de su solicitud, haga clic aquí: '
        f'http://localhost:3000/request-service/details/{service_request_id}\n\n'
        'Gracias por confiar en nosotros.'
    )
    sender = 'mdhome <neiderzamora09@gmail.com>'
    recipients = [patient.email]

    return {
        'subject': subject,
        'message': message,
        'sender': sender,
        'recipients': recipients
    }
    
def doctor_arrival_email(doctor, patient):
    """
    Generates email components to confirm the doctor's arrival.

    :param doctor: DoctorUser object who has arrived.
    :param patient: PatientUser object receiving the notification.
    :return: Dictionary with 'subject', 'message', 'sender', and 'recipients'.
    """
    subject = 'Llegada del Doctor Confirmada'
    message = (
        f'Hola {patient.first_name},\n\n'
        f'El doctor {doctor.first_name} {doctor.last_name} ha llegado a tu domicilio para brindarte el servicio solicitado.\n\n'
        'Estamos comprometidos a ofrecerte el mejor servicio posible.\n\n'
        'Gracias por confiar en nosotros.'
    )
    sender = 'mdhome <neiderzamora09@gmail.com>'
    recipients = [patient.email]

    return {
        'subject': subject,
        'message': message,
        'sender': sender,
        'recipients': recipients
    }
    
def service_end_email(doctor, patient):
    """
    Generates email components for the end of a service.

    :param doctor: DoctorUser object ending the service.
    :param patient: PatientUser object receiving the notification.
    :return: Dictionary with 'subject', 'message', 'sender', and 'recipients'.
    """
    subject = 'Servicio Finalizado'
    message = (
        f'Hola {patient.first_name},\n\n'
        f'El doctor {doctor.first_name} {doctor.last_name} ha finalizado el servicio solicitado.\n\n'
        'Esperamos que hayas quedado satisfecho con nuestro servicio.\n\n'
        'Gracias por confiar en nosotros. '
    )
    sender = 'mdhome <neiderzamora09@gmail.com>'
    recipients = [patient.email]
    
    return {
        'subject': subject,
        'message': message,
        'sender': sender,
        'recipients': recipients
    }