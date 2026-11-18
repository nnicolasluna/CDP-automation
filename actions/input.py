
import json


async def fill_input(connection, selector, value):

    javascript = f"""
    (() => {{

        const element = document.querySelector(
            {json.dumps(selector)}
        );

        if (!element) {{
            throw new Error("Input no encontrado");
        }}

        if (!["INPUT", "TEXTAREA"].includes(element.tagName)) {{
            throw new Error("El elemento no es INPUT ni TEXTAREA");
        }}

        if (element.disabled || element.readOnly) {{
            throw new Error("El campo no permite escritura");
        }}

        element.focus();

        const prototype = element.tagName === "INPUT"
            ? HTMLInputElement.prototype
            : HTMLTextAreaElement.prototype;

        const setter = Object.getOwnPropertyDescriptor(
            prototype,
            "value"
        ).set;

        setter.call(element, {json.dumps(value)});

        element.dispatchEvent(
            new Event("input", {{ bubbles: true }})
        );

        element.dispatchEvent(
            new Event("change", {{ bubbles: true }})
        );

        return {{
            success: true,
            value: element.value
        }};

    }})()
    """

    result = await connection.evaluate(javascript)

    print("Input completado:", result)

    return result
