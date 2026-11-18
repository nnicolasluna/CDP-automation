import asyncio
import os
from dotenv import load_dotenv
from browser.chrome import Chrome
from browser.connection import CDPConnection

from actions.click import click
from actions.input import fill_input
from actions.wait import wait_for_page, verify_text, wait_for_selector


load_dotenv()

GOOGLE_EMAIL = os.getenv("GOOGLE_EMAIL")
GOOGLE_PASSWORD = os.getenv("GOOGLE_PASSWORD")

CHROME_PATH = os.getenv("CHROME_PATH")
CDP_PORT = int(os.getenv("CDP_PORT", "9222"))

GOOGLE_CLOUD_URL = os.getenv("GOOGLE_CLOUD_URL")
async def main():

    browser = Chrome(
        chrome_path=CHROME_PATH,
        port=CDP_PORT
    )

    connection = CDPConnection()

    try:
        browser.start(GOOGLE_CLOUD_URL)

        await connection.connect()

        await connection.send("Runtime.enable")
        await connection.send("Page.enable")
        
        await wait_for_page(connection, timeout=30)

        await asyncio.sleep(3)
        await fill_input(
            connection,
            "#identifierId",
            GOOGLE_EMAIL
        )
        await click(
            connection,
            "#identifierNext button"
        )
        await asyncio.sleep(3)
        verified = await verify_text(
            connection,
            "Ingresa tu contraseña",
            timeout=15
        )

        if not verified:
            raise Exception(
                "No se llegó al formulario de contraseña"
            )
            
        await fill_input(
            connection,
            'input[name="Passwd"]',
            GOOGLE_PASSWORD
        )
        await click(
            connection,
            "#passwordNext button"
        )        
        verified = await verify_text(
            connection,
            "Secretos del cliente",
            timeout=15
                )
        
        if not verified:
            raise Exception(
            "No se llegó al formulario de contraseña"
            )               
        
        await asyncio.sleep(5) 
        await click(
            connection,
            'button[aria-label="Agregar secreto del cliente"]'
        )
        verified = await verify_text(
            connection,
            "NUEVO",
            timeout=15
        )
                
        if not verified:
            raise Exception(
            "Se creo nuevo secreto del cliente"
        )               
        
        await click(
            connection,
            'button[aria-label^="Cuenta:"]'
        )

        
        await wait_for_selector(
            connection,
            'a[data-test-id="sign-out-button"]',
            timeout=15
        )

        await click(
            connection,
            'a[data-test-id="sign-out-button"]'
        )
        
    finally:
        await connection.close()
        browser.close()

if __name__ == "__main__":
    asyncio.run(main())
