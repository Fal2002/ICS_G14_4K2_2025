from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class ResultadoInscripcion:
    """Resultado de una operación de inscripción"""

    exitoso: bool
    mensaje: str


class Visitante:
    """Representa un visitante con sus datos personales"""

    def __init__(
        self,
        nombre: Optional[str] = None,
        dni: Optional[int] = None,
        edad: Optional[int] = None,
        talla_vestimenta: Optional[str] = None,
    ):
        self.nombre = nombre
        self.dni = dni
        self.edad = edad
        self.talla_vestimenta = talla_vestimenta


class ServicioInscripcion:
    """
    Responsable de coordinar y validar las inscripciones.
    Centraliza todas las reglas de negocio relacionadas con inscripciones.
    """

    def inscribir_visitantes(
        self,
        actividad: "Actividad",
        horario: str,
        visitantes: List[Visitante],
        acepta_terminos: bool,
    ) -> ResultadoInscripcion:
        """
        Coordina el proceso de inscripción validando todas las reglas de negocio.

        Args:
            actividad: La actividad en la que se quiere inscribir
            horario: El horario solicitado
            visitantes: Lista de visitantes a inscribir
            acepta_terminos: Si se aceptaron los términos y condiciones

        Returns:
            ResultadoInscripcion con el resultado de la operación
        """

        # Validación 1: Reglas de negocio básicas
        resultado_validacion = self._validar_reglas_basicas(visitantes, acepta_terminos)
        if not resultado_validacion.exitoso:
            return resultado_validacion

        # Validación 2: Disponibilidad en la actividad
        resultado_validacion = self._validar_disponibilidad(
            actividad, horario, len(visitantes)
        )
        if not resultado_validacion.exitoso:
            return resultado_validacion

        # Validación 3: Datos de visitantes
        resultado_validacion = self._validar_visitantes(
            visitantes, actividad.requiere_talla
        )
        if not resultado_validacion.exitoso:
            return resultado_validacion

        # Si todas las validaciones pasaron, registrar la inscripción
        actividad.registrar_inscripcion(horario, visitantes)
        return ResultadoInscripcion(exitoso=True, mensaje="Inscripción exitosa")

    def _validar_reglas_basicas(
        self, visitantes: List[Visitante], acepta_terminos: bool
    ) -> ResultadoInscripcion:
        """
        Valida reglas básicas del proceso de inscripción.

        Args:
            visitantes: Lista de visitantes
            acepta_terminos: Si se aceptaron los términos

        Returns:
            ResultadoInscripcion con el resultado de la validación
        """

        if len(visitantes) == 0:
            return ResultadoInscripcion(
                exitoso=False, mensaje="Debe proporcionar al menos un visitante."
            )

        if not acepta_terminos:
            return ResultadoInscripcion(
                exitoso=False,
                mensaje="Debe aceptar los términos y condiciones para inscribirse.",
            )

        return ResultadoInscripcion(exitoso=True, mensaje="")

    def _validar_disponibilidad(
        self, actividad: "Actividad", horario: str, cantidad: int
    ) -> ResultadoInscripcion:
        """
        Valida que haya cupos disponibles en el horario solicitado.

        Args:
            actividad: Actividad a validar
            horario: Horario solicitado
            cantidad: Cantidad de cupos requeridos

        Returns:
            ResultadoInscripcion con el resultado de la validación
        """

        if not actividad.es_horario_valido(horario):
            return ResultadoInscripcion(
                exitoso=False, mensaje="Horario no válido o no disponible."
            )

        if actividad.obtener_cantidad_cupos_disponibles_horario(horario) < cantidad:
            return ResultadoInscripcion(
                exitoso=False,
                mensaje="No hay suficientes cupos disponibles para el horario solicitado.",
            )

        return ResultadoInscripcion(exitoso=True, mensaje="")

    def _validar_visitantes(
        self, visitantes: List[Visitante], requiere_talla: bool
    ) -> ResultadoInscripcion:
        """
        Valida que todos los visitantes tengan los datos requeridos.

        Args:
            visitantes: Lista de visitantes a validar
            requiere_talla: Si la actividad requiere talla

        Returns:
            ResultadoInscripcion con el resultado de la validación
        """

        for visitante in visitantes:
            # validar que el nombre no tenga numeros o caracteres especiales
            if not visitante.nombre or not all(
                c.isalpha() or c.isspace() for c in visitante.nombre
            ):
                return ResultadoInscripcion(
                    exitoso=False,
                    mensaje="Todos los visitantes deben tener un nombre válido (sin números ni caracteres especiales).",
                )
            # Validar que sea un número entero positivo
            if (
                not visitante.dni
                or not isinstance(visitante.dni, int)
                or visitante.dni <= 0
            ):
                return ResultadoInscripcion(
                    exitoso=False,
                    mensaje="Todos los visitantes deben tener un DNI válido (número entero positivo).",
                )
            if not visitante.edad or visitante.edad <= 0:
                return ResultadoInscripcion(
                    exitoso=False,
                    mensaje="Todos los visitantes deben tener una edad válida (número positivo).",
                )
            if requiere_talla:
                if (
                    not visitante.talla_vestimenta
                    or visitante.talla_vestimenta not in ["XS", "S", "M", "L", "XL"]
                ):
                    return ResultadoInscripcion(
                        exitoso=False,
                        mensaje="Debe proporcionar una talla de vestimenta para cada visitante para esta actividad (XS, S, M, L, XL).",
                    )

        return ResultadoInscripcion(exitoso=True, mensaje="")


class Actividad:
    """
    Representa una actividad con sus horarios y cupos.
    Responsable solo de gestionar su configuración y estado.
    """

    def __init__(
        self, nombre: str, horarios: Dict[str, int], requiere_talla: bool = False
    ):
        """
        Inicializa una actividad.

        Args:
            nombre: Nombre de la actividad
            horarios: Diccionario de horarios con cupos disponibles (ej: {"10": 15})
            requiere_talla: Si la actividad requiere talla de vestimenta
        """
        self.nombre = nombre
        self.horarios = horarios
        self.requiere_talla = requiere_talla
        self.inscripciones_por_horario = {h: [] for h in horarios}

    def registrar_inscripcion(self, horario: str, visitantes: List[Visitante]) -> None:
        """
        Registra la inscripción de visitantes en un horario específico.
        Este método NO realiza validaciones, solo actualiza el estado.

        Args:
            horario: Horario en el que se inscribe
            visitantes: Lista de visitantes a inscribir
        """
        self.inscripciones_por_horario[horario].extend(visitantes)

    def obtener_cantidad_cupos_disponibles_horario(self, horario: str) -> int:
        """
        Devuelve la cantidad de cupos disponibles para un horario.

        Args:
            horario: Horario a consultar

        Returns:
            Cantidad de cupos disponibles
        """
        cupos_totales = self.horarios.get(horario, 0)
        inscriptos = len(self.inscripciones_por_horario.get(horario, []))
        return cupos_totales - inscriptos

    def es_horario_valido(self, horario: str) -> bool:
        """
        Indica si el horario pertenece a la actividad.

        Args:
            horario: Horario a validar

        Returns:
            True si el horario es válido, False en caso contrario
        """
        return horario in self.horarios


class GestorActividades:
    """
    Gestor central de actividades.
    Mantiene el catálogo de actividades y coordina las inscripciones.
    """

    def __init__(self):
        """Inicializa el gestor con el catálogo de actividades predefinidas"""
        self.actividades: Dict[str, Actividad] = {
            "Tirolesa": Actividad(
                "Tirolesa",
                {
                    "10": 10,
                    "11": 10,
                    "12": 10,
                    "13": 10,
                    "14": 10,
                    "15": 10,
                    "16": 10,
                    "17": 10,
                },
                requiere_talla=True,
            ),
            "Palestra": Actividad(
                "Palestra",
                {
                    "10": 12,
                    "11": 12,
                    "12": 12,
                    "13": 12,
                    "14": 12,
                    "15": 12,
                    "16": 12,
                    "17": 12,
                },
                requiere_talla=True,
            ),
            "Jardinería": Actividad(
                "Jardinería",
                {
                    "10": 12,
                    "11": 12,
                    "12": 12,
                    "13": 12,
                    "14": 12,
                    "15": 12,
                    "16": 12,
                    "17": 12,
                },
                requiere_talla=False,
            ),
            "Safari": Actividad(
                "Safari",
                {
                    "10": 8,
                    "11": 8,
                    "12": 8,
                    "13": 8,
                    "14": 8,
                    "15": 8,
                    "16": 8,
                    "17": 8,
                },
                requiere_talla=False,
            ),
        }
        self._servicio_inscripcion = ServicioInscripcion()

    def agregar_actividad(self, actividad: Actividad) -> None:
        """
        Agrega una nueva actividad al catálogo.

        Args:
            actividad: Actividad a agregar
        """
        self.actividades[actividad.nombre] = actividad

    def obtener_actividad(self, nombre: str) -> Optional[Actividad]:
        """
        Obtiene una actividad por su nombre.

        Args:
            nombre: Nombre de la actividad

        Returns:
            La actividad solicitada o None si no existe
        """
        return self.actividades.get(nombre)

    def registrar_inscripcion(
        self,
        nombre_actividad: str,
        horario: str,
        visitantes: List[Visitante],
        acepta_terminos: bool,
    ) -> ResultadoInscripcion:
        """
        Registra una inscripción para una actividad específica.
        Valida que la actividad exista y delega al servicio de inscripción.

        Args:
            nombre_actividad: Nombre de la actividad
            horario: Horario solicitado
            visitantes: Lista de visitantes
            acepta_terminos: Si se aceptaron los términos y condiciones

        Returns:
            ResultadoInscripcion con el resultado de la operación
        """
        actividad = self.obtener_actividad(nombre_actividad)
        if not actividad:
            return ResultadoInscripcion(
                exitoso=False, mensaje="La actividad solicitada no existe."
            )

        # Delega al servicio de inscripción
        return self._servicio_inscripcion.inscribir_visitantes(
            actividad, horario, visitantes, acepta_terminos
        )
