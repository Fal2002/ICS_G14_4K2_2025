import pytest

from models import Actividad, Visitante, GestorActividades, ServicioInscripcion


# ========== FIXTURES ==========
@pytest.fixture
def servicio_inscripcion():
    """Fixture que proporciona una instancia del servicio de inscripción"""
    return ServicioInscripcion()


@pytest.fixture
def gestor():
    """Fixture que proporciona un gestor de actividades vacío"""
    return GestorActividades()


@pytest.fixture
def actividad_con_cupos():
    """Fixture que proporciona una actividad con cupos disponibles"""
    return Actividad(
        nombre="Tirolesa", horarios={"10": 10, "11": 2}, requiere_talla=True
    )


@pytest.fixture
def actividad_sin_cupos():
    """Fixture que proporciona una actividad sin cupos"""
    return Actividad(nombre="Tirolesa", horarios={"10": 0}, requiere_talla=True)


@pytest.fixture
def actividad_sin_talla_requerida():
    """Fixture que proporciona una actividad que no requiere talla"""
    return Actividad(nombre="Paseo en bote", horarios={"11": 5}, requiere_talla=False)


@pytest.fixture
def actividad_multiples_horarios():
    """Fixture que proporciona una actividad con múltiples horarios"""
    return Actividad(
        nombre="Escalada", horarios={"09": 10, "14": 10}, requiere_talla=True
    )


@pytest.fixture
def visitante_completo():
    """Fixture que proporciona un visitante con todos los datos válidos"""
    return Visitante(nombre="Juan Pérez", dni=12345678, edad=30, talla_vestimenta="M")


@pytest.fixture
def visitante_sin_talla():
    """Fixture que proporciona un visitante sin talla"""
    return Visitante(nombre="SofiaLopez", dni=33445566, edad=27)


@pytest.fixture
def visitante_sin_nombre():
    """Fixture que proporciona un visitante sin nombre"""
    return Visitante(dni=44556677, edad=31, talla_vestimenta="M")


@pytest.fixture
def visitante_sin_dni():
    """Fixture que proporciona un visitante sin DNI"""
    return Visitante(nombre="ElenaFernandez", edad=26, talla_vestimenta="S")


@pytest.fixture
def visitante_sin_edad():
    """Fixture que proporciona un visitante sin edad"""
    return Visitante(nombre="PedroSanchez", dni=22334455, talla_vestimenta="L")


class TestInscripcionActividad:

    def test_inscripcion_actividad_inexistente(self, gestor):
        # ========== ARRANGE ==========
        print("\n--- Test: Inscripción a actividad inexistente ---")
        visitantes = [
            Visitante(
                nombre="Pedro Sánchez", dni=22334455, edad=40, talla_vestimenta="L"
            )
        ]
        print(f"Visitante creado: {visitantes[0].nombre}")

        # ========== ACT ==========
        print("Intentando inscribir a actividad 'ActividadInexistente'...")
        resultado = gestor.registrar_inscripcion(
            nombre_actividad="ActividadInexistente",
            horario="10",
            visitantes=visitantes,
            acepta_terminos=True,
        )

        # ========== ASSERT ==========
        print(f"Resultado: {resultado.mensaje}")
        assert resultado.exitoso is False
        assert "no existe" in resultado.mensaje.lower()
        print("✓ Test pasado: Inscripción rechazada correctamente")

    def test_inscripcion_exitosa_unico_visitante_con_cupo_y_todos_los_campos_validos(
        self, servicio_inscripcion, actividad_con_cupos, visitante_completo
    ):
        # ========== ACT ==========
        print("\n--- Test: Inscripción exitosa con un visitante ---")
        print(f"Actividad: {actividad_con_cupos.nombre}, Horario: 10:00")
        print(
            f"Cupos disponibles antes: {actividad_con_cupos.obtener_cantidad_cupos_disponibles_horario('10')}"
        )
        print(
            f"Visitante: {visitante_completo.nombre} (DNI: {visitante_completo.dni}, Talla: {visitante_completo.talla_vestimenta})"
        )

        resultado = servicio_inscripcion.inscribir_visitantes(
            actividad=actividad_con_cupos,
            horario="10",
            visitantes=[visitante_completo],
            acepta_terminos=True,
        )

        # ========== ASSERT ==========
        print(f"Resultado: {resultado.mensaje}")
        print(
            f"Cupos disponibles después: {actividad_con_cupos.obtener_cantidad_cupos_disponibles_horario('10')}"
        )
        assert resultado.exitoso is True
        assert "exitosa" in resultado.mensaje.lower()
        assert actividad_con_cupos.obtener_cantidad_cupos_disponibles_horario("10") == 9
        print("✓ Test pasado: Inscripción exitosa y cupo actualizado")

    def test_inscripcion_exitosa_multiples_visitantes_con_cupo_y_todos_los_campos_validos(
        self, servicio_inscripcion, actividad_con_cupos
    ):
        # ========== ARRANGE ==========
        print("\n--- Test: Inscripción exitosa con múltiples visitantes ---")
        visitantes = [
            Visitante(nombre="Ana Gómez", dni=87654321, edad=28, talla_vestimenta="S"),
            Visitante(
                nombre="Luis Martínez", dni=11223344, edad=35, talla_vestimenta="L"
            ),
        ]
        print(f"Actividad: {actividad_con_cupos.nombre}, Horario: 10:00")
        print(
            f"Cupos disponibles antes: {actividad_con_cupos.obtener_cantidad_cupos_disponibles_horario('10')}"
        )
        print(f"Cantidad de visitantes: {len(visitantes)}")
        for v in visitantes:
            print(f"  - {v.nombre} (DNI: {v.dni}, Talla: {v.talla_vestimenta})")

        # ========== ACT ==========
        resultado = servicio_inscripcion.inscribir_visitantes(
            actividad=actividad_con_cupos,
            horario="10",
            visitantes=visitantes,
            acepta_terminos=True,
        )

        # ========== ASSERT ==========
        print(f"Resultado: {resultado.mensaje}")
        print(
            f"Cupos disponibles después: {actividad_con_cupos.obtener_cantidad_cupos_disponibles_horario('10')}"
        )
        assert resultado.exitoso is True
        assert "exitosa" in resultado.mensaje.lower()
        assert actividad_con_cupos.obtener_cantidad_cupos_disponibles_horario("10") == 8
        print("✓ Test pasado: Inscripción múltiple exitosa y cupos actualizados")

    def test_inscripcion_fallida_sin_cupo_un_visitante(
        self, servicio_inscripcion, actividad_sin_cupos, visitante_completo
    ):
        # ========== ACT ==========
        print("\n--- Test: Inscripción fallida por falta de cupos ---")
        print(f"Actividad: {actividad_sin_cupos.nombre}, Horario: 10:00")
        print(
            f"Cupos disponibles: {actividad_sin_cupos.obtener_cantidad_cupos_disponibles_horario('10')}"
        )
        print(f"Visitante: {visitante_completo.nombre}")

        resultado = servicio_inscripcion.inscribir_visitantes(
            actividad=actividad_sin_cupos,
            horario="10",
            visitantes=[visitante_completo],
            acepta_terminos=True,
        )

        # ========== ASSERT ==========
        print(f"Resultado: {resultado.mensaje}")
        assert resultado.exitoso is False
        assert "cupos" in resultado.mensaje.lower()
        assert actividad_sin_cupos.obtener_cantidad_cupos_disponibles_horario("10") == 0
        print("✓ Test pasado: Inscripción rechazada por falta de cupos")

    def test_inscripcion_fallida_por_cupo_insuficiente_para_multiples_visitantes(
        self, servicio_inscripcion, actividad_con_cupos
    ):
        # ========== ARRANGE ==========
        print(
            "\n--- Test: Inscripción fallida por cupo insuficiente para múltiples visitantes ---"
        )
        visitantes = [
            Visitante(nombre="Ana Gómez", dni=87654321, edad=28, talla_vestimenta="S"),
            Visitante(
                nombre="Luis Martínez", dni=11223344, edad=35, talla_vestimenta="L"
            ),
            Visitante(
                nombre="Carlos Ruiz", dni=55667788, edad=22, talla_vestimenta="M"
            ),
        ]
        print(f"Actividad: {actividad_con_cupos.nombre}, Horario: 10:00")
        print(
            f"Cupos disponibles antes: {actividad_con_cupos.obtener_cantidad_cupos_disponibles_horario('11')}"
        )
        print(f"Cantidad de visitantes: {len(visitantes)}")
        for v in visitantes:
            print(f"  - {v.nombre} (DNI: {v.dni}, Talla: {v.talla_vestimenta})")

        # ========== ACT ==========
        resultado = servicio_inscripcion.inscribir_visitantes(
            actividad=actividad_con_cupos,
            horario="11",
            visitantes=visitantes,
            acepta_terminos=True,
        )

        # ========== ASSERT ==========
        print(f"Resultado: {resultado.mensaje}")
        assert resultado.exitoso is False
        assert "cupos" in resultado.mensaje.lower()
        assert (
            actividad_con_cupos.obtener_cantidad_cupos_disponibles_horario("10") == 10
        )
        print("✓ Test pasado: Inscripción rechazada por cupo insuficiente")

    def test_inscripcion_sin_talla_para_actividad_con_talla_requerida(
        self, servicio_inscripcion, actividad_con_cupos, visitante_sin_talla
    ):
        # ========== ACT ==========
        print("\n--- Test: Inscripción sin talla para actividad que la requiere ---")
        print(
            f"Actividad: {actividad_con_cupos.nombre} (Requiere talla: {actividad_con_cupos.requiere_talla})"
        )
        print(
            f"Visitante: {visitante_sin_talla.nombre} (Talla: {visitante_sin_talla.talla_vestimenta})"
        )

        resultado = servicio_inscripcion.inscribir_visitantes(
            actividad=actividad_con_cupos,
            horario="10",
            visitantes=[visitante_sin_talla],
            acepta_terminos=True,
        )

        # ========== ASSERT ==========
        print(f"Resultado: {resultado.mensaje}")
        assert resultado.exitoso is False
        assert "talla" in resultado.mensaje.lower()
        assert (
            actividad_con_cupos.obtener_cantidad_cupos_disponibles_horario("10") == 10
        )
        print("✓ Test pasado: Inscripción rechazada por falta de talla")

    def test_inscripcion_sin_talla_para_actividad_sin_talla_requerida(
        self, servicio_inscripcion, actividad_sin_talla_requerida, visitante_sin_talla
    ):
        # ========== ACT ==========
        print("\n--- Test: Inscripción sin talla para actividad que NO la requiere ---")
        print(
            f"Actividad: {actividad_sin_talla_requerida.nombre} (Requiere talla: {actividad_sin_talla_requerida.requiere_talla})"
        )
        print(
            f"Visitante: {visitante_sin_talla.nombre} (Talla: {visitante_sin_talla.talla_vestimenta})"
        )
        print(
            f"Cupos disponibles antes: {actividad_sin_talla_requerida.obtener_cantidad_cupos_disponibles_horario('11')}"
        )

        resultado = servicio_inscripcion.inscribir_visitantes(
            actividad=actividad_sin_talla_requerida,
            horario="11",
            visitantes=[visitante_sin_talla],
            acepta_terminos=True,
        )

        # ========== ASSERT ==========
        print(f"Resultado: {resultado.mensaje}")
        print(
            f"Cupos disponibles después: {actividad_sin_talla_requerida.obtener_cantidad_cupos_disponibles_horario('11')}"
        )
        assert resultado.exitoso is True
        assert "exitosa" in resultado.mensaje.lower()
        assert (
            actividad_sin_talla_requerida.obtener_cantidad_cupos_disponibles_horario(
                "11"
            )
            == 4
        )
        print("✓ Test pasado: Inscripción exitosa sin talla requerida")

    def test_inscripcion_fallida_por_horario_invalido(
        self, servicio_inscripcion, actividad_multiples_horarios, visitante_completo
    ):
        # ========== ACT ==========
        print("\n--- Test: Inscripción con horario inválido ---")
        print(f"Actividad: {actividad_multiples_horarios.nombre}")
        print(
            f"Horarios disponibles: {list(actividad_multiples_horarios.horarios.keys())}"
        )
        print(f"Horario solicitado: 12:00 (inválido)")

        resultado = servicio_inscripcion.inscribir_visitantes(
            actividad=actividad_multiples_horarios,
            horario="12",  # Horario inválido
            visitantes=[visitante_completo],
            acepta_terminos=True,
        )

        # ========== ASSERT ==========
        print(f"Resultado: {resultado.mensaje}")
        assert resultado.exitoso is False
        assert "horario no válido" in resultado.mensaje.lower()
        assert (
            actividad_multiples_horarios.obtener_cantidad_cupos_disponibles_horario(
                "09"
            )
            == 10
        )
        assert (
            actividad_multiples_horarios.obtener_cantidad_cupos_disponibles_horario(
                "14"
            )
            == 10
        )
        print("✓ Test pasado: Inscripción rechazada por horario inválido")

    def test_inscripcion_sin_aceptar_terminos(
        self, servicio_inscripcion, actividad_con_cupos, visitante_completo
    ):
        # ========== ACT ==========
        print("\n--- Test: Inscripción sin aceptar términos y condiciones ---")
        print(f"Visitante: {visitante_completo.nombre}")
        print(f"Acepta términos: False")

        resultado = servicio_inscripcion.inscribir_visitantes(
            actividad=actividad_con_cupos,
            horario="10",
            visitantes=[visitante_completo],
            acepta_terminos=False,  # No acepta términos
        )

        # ========== ASSERT ==========
        print(f"Resultado: {resultado.mensaje}")
        assert resultado.exitoso is False
        assert "términos" in resultado.mensaje.lower()
        assert (
            actividad_con_cupos.obtener_cantidad_cupos_disponibles_horario("10") == 10
        )
        print("✓ Test pasado: Inscripción rechazada por no aceptar términos")

    def test_inscripcion_sin_nombre_visitante(
        self, servicio_inscripcion, actividad_con_cupos, visitante_sin_nombre
    ):
        # ========== ACT ==========
        print("\n--- Test: Inscripción sin nombre de visitante ---")
        print(f"Visitante nombre: {visitante_sin_nombre.nombre}")
        print(f"Visitante DNI: {visitante_sin_nombre.dni}")

        resultado = servicio_inscripcion.inscribir_visitantes(
            actividad=actividad_con_cupos,
            horario="10",
            visitantes=[visitante_sin_nombre],
            acepta_terminos=True,
        )

        # ========== ASSERT ==========
        print(f"Resultado: {resultado.mensaje}")
        assert resultado.exitoso is False
        assert "nombre" in resultado.mensaje.lower()
        assert (
            actividad_con_cupos.obtener_cantidad_cupos_disponibles_horario("10") == 10
        )
        print("✓ Test pasado: Inscripción rechazada por falta de nombre")

    def test_inscripcion_sin_dni_visitante(
        self, servicio_inscripcion, actividad_con_cupos, visitante_sin_dni
    ):
        # ========== ACT ==========
        print("\n--- Test: Inscripción sin DNI de visitante ---")
        print(f"Visitante nombre: {visitante_sin_dni.nombre}")
        print(f"Visitante DNI: {visitante_sin_dni.dni}")

        resultado = servicio_inscripcion.inscribir_visitantes(
            actividad=actividad_con_cupos,
            horario="10",
            visitantes=[visitante_sin_dni],
            acepta_terminos=True,
        )

        # ========== ASSERT ==========
        print(f"Resultado: {resultado.mensaje}")
        assert resultado.exitoso is False
        assert "dni" in resultado.mensaje.lower()
        assert (
            actividad_con_cupos.obtener_cantidad_cupos_disponibles_horario("10") == 10
        )
        print("✓ Test pasado: Inscripción rechazada por falta de DNI")

    def test_inscripcion_sin_edad_visitante(
        self, servicio_inscripcion, actividad_con_cupos, visitante_sin_edad
    ):
        # ========== ACT ==========
        print("\n--- Test: Inscripción sin edad de visitante ---")
        print(f"Visitante nombre: {visitante_sin_edad.nombre}")
        print(f"Visitante edad: {visitante_sin_edad.edad}")

        resultado = servicio_inscripcion.inscribir_visitantes(
            actividad=actividad_con_cupos,
            horario="10",
            visitantes=[visitante_sin_edad],
            acepta_terminos=True,
        )

        # ========== ASSERT ==========
        print(f"Resultado: {resultado.mensaje}")
        assert resultado.exitoso is False
        assert "edad" in resultado.mensaje.lower()
        assert (
            actividad_con_cupos.obtener_cantidad_cupos_disponibles_horario("10") == 10
        )
        print("✓ Test pasado: Inscripción rechazada por falta de edad")

    def test_inscripcion_sin_visitantes(
        self, servicio_inscripcion, actividad_con_cupos
    ):
        # ========== ACT ==========
        print("\n--- Test: Inscripción sin visitantes ---")
        print(f"Actividad: {actividad_con_cupos.nombre}")
        print(f"Cantidad de visitantes: 0")

        resultado = servicio_inscripcion.inscribir_visitantes(
            actividad=actividad_con_cupos,
            horario="10",
            visitantes=[],
            acepta_terminos=True,
        )

        # ========== ASSERT ==========
        print(f"Resultado: {resultado.mensaje}")
        assert resultado.exitoso is False
        assert "al menos un visitante" in resultado.mensaje.lower()
        assert (
            actividad_con_cupos.obtener_cantidad_cupos_disponibles_horario("10") == 10
        )
        print("✓ Test pasado: Inscripción rechazada por falta de visitantes")

    def test_inscripcion_con_nombre_invalido(
        self, servicio_inscripcion, actividad_con_cupos
    ):
        # ========== ARRANGE ==========
        print("\n--- Test: Inscripción con nombre de visitante inválido ---")
        visitante_nombre_invalido = Visitante(
            nombre="Juan123", dni=12345678, edad=30, talla_vestimenta="M"
        )
        print(f"Visitante con nombre inválido: {visitante_nombre_invalido.nombre}")

        # ========== ACT ==========
        resultado = servicio_inscripcion.inscribir_visitantes(
            actividad=actividad_con_cupos,
            horario="10",
            visitantes=[visitante_nombre_invalido],
            acepta_terminos=True,
        )

        # ========== ASSERT ==========
        print(f"Resultado: {resultado.mensaje}")
        assert resultado.exitoso is False
        assert "nombre válido" in resultado.mensaje.lower()
        assert (
            actividad_con_cupos.obtener_cantidad_cupos_disponibles_horario("10") == 10
        )
        print("✓ Test pasado: Inscripción rechazada por nombre inválido")

    def test_inscripcion_con_dni_invalido(
        self, servicio_inscripcion, actividad_con_cupos
    ):
        # ========== ARRANGE ==========
        print("\n--- Test: Inscripción con DNI de visitante inválido (negativo) ---")
        visitante_dni_invalido = Visitante(
            nombre="Juan Perez", dni=-12345678, edad=30, talla_vestimenta="M"
        )
        print(f"Visitante con DNI inválido: {visitante_dni_invalido.dni}")

        # ========== ACT ==========
        resultado = servicio_inscripcion.inscribir_visitantes(
            actividad=actividad_con_cupos,
            horario="10",
            visitantes=[visitante_dni_invalido],
            acepta_terminos=True,
        )

        # ========== ASSERT ==========
        print(f"Resultado: {resultado.mensaje}")
        assert resultado.exitoso is False
        assert "dni válido" in resultado.mensaje.lower()
        assert (
            actividad_con_cupos.obtener_cantidad_cupos_disponibles_horario("10") == 10
        )
        print("✓ Test pasado: Inscripción rechazada por DNI inválido")

    def test_inscripcion_con_edad_invalida(
        self, servicio_inscripcion, actividad_con_cupos
    ):
        # ========== ARRANGE ==========
        print("\n--- Test: Inscripción con edad de visitante inválida (cero) ---")
        visitante_edad_invalida = Visitante(
            nombre="Juan Perez", dni=12345678, edad=0, talla_vestimenta="M"
        )
        print(f"Visitante con edad inválida: {visitante_edad_invalida.edad}")

        # ========== ACT ==========
        resultado = servicio_inscripcion.inscribir_visitantes(
            actividad=actividad_con_cupos,
            horario="10",
            visitantes=[visitante_edad_invalida],
            acepta_terminos=True,
        )

        # ========== ASSERT ==========
        print(f"Resultado: {resultado.mensaje}")
        assert resultado.exitoso is False
        assert "edad válida" in resultado.mensaje.lower()
        assert (
            actividad_con_cupos.obtener_cantidad_cupos_disponibles_horario("10") == 10
        )
        print("✓ Test pasado: Inscripción rechazada por edad inválida")

    def test_inscripcion_con_talla_invalida(
        self, servicio_inscripcion, actividad_con_cupos
    ):
        # ========== ARRANGE ==========
        print("\n--- Test: Inscripción con talla de vestimenta inválida ---")
        visitante_talla_invalida = Visitante(
            nombre="Juan Perez", dni=12345678, edad=30, talla_vestimenta="XXL"
        )
        print(
            f"Visitante con talla inválida: {visitante_talla_invalida.talla_vestimenta}"
        )

        # ========== ACT ==========
        resultado = servicio_inscripcion.inscribir_visitantes(
            actividad=actividad_con_cupos,
            horario="10",
            visitantes=[visitante_talla_invalida],
            acepta_terminos=True,
        )

        # ========== ASSERT ==========
        print(f"Resultado: {resultado.mensaje}")
        assert resultado.exitoso is False
        assert "talla de vestimenta" in resultado.mensaje.lower()
        assert (
            actividad_con_cupos.obtener_cantidad_cupos_disponibles_horario("10") == 10
        )
        print("✓ Test pasado: Inscripción rechazada por talla inválida")
