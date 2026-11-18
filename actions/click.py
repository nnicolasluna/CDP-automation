
import json


async def click(connection, selector):

    javascript = f"""
    (() => {{

        const element = document.querySelector(
            {json.dumps(selector)}
        );

        if (!element) {{
            throw new Error("Elemento no encontrado: " + {json.dumps(selector)});
        }}

        if (element.disabled) {{
            throw new Error("El elemento está deshabilitado");
        }}

        element.click();

        return {{
            success: true,
            element: element.tagName
        }};

    }})()
    """

    result = await connection.evaluate(javascript)

    print("Click ejecutado:", result)

    return result
