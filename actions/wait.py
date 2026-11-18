
import asyncio
import json


async def wait_for_page(connection, timeout=30):

    elapsed = 0

    while elapsed < timeout:

        ready_state = await connection.evaluate(
            "document.readyState"
        )

        if ready_state == "complete":
            print("La página terminó de cargar")
            return True

        await asyncio.sleep(0.5)
        elapsed += 0.5

    raise TimeoutError(
        f"La página no terminó de cargar en {timeout} segundos"
    )


async def verify_text(connection, expected_text, timeout=10):

    elapsed = 0

    while elapsed < timeout:

        javascript = f"""
        (() => {{
            const pageText = document.body
                ? document.body.innerText
                : "";

            return pageText.includes({json.dumps(expected_text)});
        }})()
        """

        found = await connection.evaluate(javascript)

        if found:
            print(f"Verificación correcta: '{expected_text}'")
            return True

        await asyncio.sleep(0.5)
        elapsed += 0.5

    print(f"No se encontró el texto: '{expected_text}'")
    return False

async def wait_for_selector(connection, selector, timeout=15):

    elapsed = 0

    while elapsed < timeout:

        found = await connection.evaluate(f"""
            document.querySelector(
                {json.dumps(selector)}
            ) !== null
        """)

        if found:
            print(f"Elemento encontrado: {selector}")
            return True

        await asyncio.sleep(0.5)
        elapsed += 0.5

    raise TimeoutError(
        f"No apareció el elemento: {selector}"
    )
