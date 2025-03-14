import time
import re
from kittycad.api.ml import create_text_to_cad, get_text_to_cad_model_for_user
from kittycad.client import ClientFromEnv
from kittycad.models import (
    ApiCallStatus,
    Error,
    FileExportFormat,
    TextToCad,
    TextToCadCreateBody,
)

def sanitize_filename(prompt: str) -> str:
    """
    Convert the input prompt into a safe file name by replacing spaces and 
    removing any non-alphanumeric characters. This simple sanitization replaces 
    spaces with underscores and removes characters that are not letters, numbers, 
    or underscores.
    """
    safe = re.sub(r'[^a-zA-Z0-9_]', '', prompt.strip().replace(' ', '_'))
    return safe

def main():
    # Prompt the user to enter a text prompt for the CAD model.
    user_prompt = input("Enter your CAD prompt: ")
    
    # Create a safe file name from the prompt.
    safe_filename = sanitize_filename(user_prompt) + ".obj"
    
    # Create our client using the API token from the environment variable ZOO_API_TOKEN.
    client = ClientFromEnv()

    # Submit the prompt to generate a CAD model in OBJ format.
    response = create_text_to_cad.sync(
        client=client,
        output_format=FileExportFormat.OBJ,  # Change to OBJ format
        body=TextToCadCreateBody(
            prompt=user_prompt,
        ),
    )

    if isinstance(response, Error) or response is None:
        print(f"Error: {response}")
        exit(1)

    result: TextToCad = response

    # Poll until the CAD model generation is complete.
    while result.completed_at is None:
        time.sleep(5)  # Wait for 5 seconds before checking again
        response = get_text_to_cad_model_for_user.sync(
            client=client,
            id=result.id,
        )
        if isinstance(response, Error) or response is None:
            print(f"Error: {response}")
            exit(1)
        result = response

    # Check the final status and handle the output.
    if result.status == ApiCallStatus.FAILED:
        print(f"Text-to-CAD failed: {result.error}")
    elif result.status == ApiCallStatus.COMPLETED:
        if result.outputs is None:
            print("Text-to-CAD completed but returned no files.")
            exit(0)

        print(f"Text-to-CAD completed and returned {len(result.outputs)} files:")
        for name in result.outputs:
            print(f"  * {name}")

        # Save the OBJ output to a file with the sanitized prompt as the file name.
        final_result = result.outputs["source.obj"]  # Change to .obj
        with open(safe_filename, "wb") as output_file:
            output_file.write(final_result)
            print(f"Saved output to {output_file.name}")

if __name__ == '__main__':
    main()
