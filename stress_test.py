import os
import time
import re
from datetime import datetime
from kittycad.api.ml import create_text_to_cad, get_text_to_cad_model_for_user
from kittycad.client import ClientFromEnv
from kittycad.models import (
    ApiCallStatus,
    Error,
    FileExportFormat,
    TextToCad,
    TextToCadCreateBody,
)

# Ensure necessary directories exist
os.makedirs("stress_test_files2", exist_ok=True)

# Output log file
LOG_FILE = "stress_test_results.txt"

# List of prompts for stress testing (Simple + Complex)
TEST_PROMPTS = [
    # # Very Simple Tools
    # "Hammer",
    # "Shovel",
    # "Screwdriver",
    # "Wrench",
    # "Pliers",
    # "Saw",
    # "Drill",
    # "Chisel",
    # "Tape Measure",
    # "Clamp",

    # # More Detailed Descriptions
    # "Heavy-duty sledgehammer with reinforced steel head",
    # "Flathead screwdriver with ergonomic rubber handle",
    # "Industrial-grade adjustable wrench with precise measurements",
    # "Circular saw blade with 24 teeth",
    # "Precision-calibrated calipers with digital display",
    # "Cordless drill body with replaceable battery pack",
    # "Socket wrench with full ratchet mechanism",
    # "Carpenter's square ruler with laser-etched measurements",
    # "Advanced multi-tool with knife, screwdriver, and pliers",
    # "Spring-loaded nail gun",
    # "Machinist's micrometer for precise internal measurements",
    # "Pipe wrench for plumbing applications",
    # "Complex interlocking gears for mechanical clock",
    # "Hacksaw frame with removable blade",

    # Common Household & Office Objects
    "Cup",
    "Table",
    "Chair",
    "Spoon",
    "Fork",
    "Plate",
    "Lamp",
    "Laptop Stand",
    "Phone Holder",
    "Water Bottle",

    # Basic Mechanical & Industrial Parts
    "Simple Gear",
    "Bolt",
    "Nut",
    "Washer",
    "Hinge",
    "Lever",
    "Pulley",
    "Fan Blade",
    "Pipe Fitting",
    "Bearing",

    # Engineering & Precise CAD Models
    "Plank 6x4 inches with four M4 screw holes in each corner with filleted edges",
    "Metal bracket with three evenly spaced 10mm holes",
    "L-bracket with 1/4-inch mounting holes and a 45-degree support beam",
    "Custom fan grille with circular venting pattern",
    "3D-printed hinge with built-in rotation stop",
    "Adjustable height desk leg mount with screw slots",
    "Enclosure for Arduino Uno with precise cutouts",
    "Heat sink with 15 vertical fins spaced 2mm apart",
    "Bicycle pedal with anti-slip texture",
    "Mechanical coupling with hexagonal inner bore",
]

def sanitize_filename(prompt: str) -> str:
    """ Convert the input prompt into a safe file name. """
    safe = re.sub(r'[^a-zA-Z0-9_]', '', prompt.strip().replace(' ', '_'))
    return safe

def log_result(prompt, status, details):
    """ Log test results into a readable output file. """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] Prompt: {prompt}\nStatus: {status}\nDetails: {details}\n{'-'*50}\n"

    with open(LOG_FILE, "a") as log_file:
        log_file.write(log_entry)

def generate_cad_model(prompt):
    """ Submits a text prompt to the API to generate a CAD model and logs results. """
    client = ClientFromEnv()
    safe_filename = f"stress_test_files2/{sanitize_filename(prompt)}.stl"

    print(f"Generating CAD model for: {prompt}...")

    response = create_text_to_cad.sync(
        client=client,
        output_format=FileExportFormat.STL,
        body=TextToCadCreateBody(prompt=prompt),
    )

    if isinstance(response, Error) or response is None:
        error_message = f"API Error: {response}"
        print(f"❌ {error_message}")
        log_result(prompt, "Failed", error_message)
        return None

    result: TextToCad = response

    # Poll until the CAD model generation is complete
    while result.completed_at is None:
        time.sleep(5)
        response = get_text_to_cad_model_for_user.sync(client=client, id=result.id)
        if isinstance(response, Error) or response is None:
            error_message = f"Polling Error: {response}"
            print(f"❌ {error_message}")
            log_result(prompt, "Failed", error_message)
            return None
        result = response

    if result.status == ApiCallStatus.FAILED:
        error_message = f"Generation failed: {result.error}"
        print(f"❌ {error_message}")
        log_result(prompt, "Failed", error_message)
        return None
    
    if result.outputs is None:
        error_message = "Generation completed but no files were returned."
        print(f"❌ {error_message}")
        log_result(prompt, "Failed", error_message)
        return None

    # Save STL file
    final_result = result.outputs.get("source.stl")
    if final_result:
        with open(safe_filename, "wb") as output_file:
            output_file.write(final_result)
        print(f"✅ Model saved: {safe_filename}")
        log_result(prompt, "Success", f"File saved as: {safe_filename}")
        return safe_filename
    else:
        error_message = "No STL output was returned by the API."
        print(f"⚠️ {error_message}")
        log_result(prompt, "Failed", error_message)
        return None

def run_stress_test():
    """ Runs the stress test by generating multiple CAD models. """
    print("\n🚀 Starting Stress Test: Generating multiple CAD models...\n")

    # Clear log file before running new tests
    with open(LOG_FILE, "w") as log_file:
        log_file.write("🚀 Text-to-CAD Stress Test Results\n")
        log_file.write(f"Test started on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write("="*60 + "\n")

    success_count = 0
    failure_count = 0

    for prompt in TEST_PROMPTS:
        result = generate_cad_model(prompt)
        if result:
            success_count += 1
        else:
            failure_count += 1

    print("\n🎯 Stress Test Completed!")
    print(f"✅ Successful Generations: {success_count}")
    print(f"❌ Failed Generations: {failure_count}")

    # Append summary to log file
    with open(LOG_FILE, "a") as log_file:
        log_file.write("\n🎯 Stress Test Summary\n")
        log_file.write(f"✅ Successful Generations: {success_count}\n")
        log_file.write(f"❌ Failed Generations: {failure_count}\n")
        log_file.write("="*60 + "\n")

if __name__ == "__main__":
    run_stress_test()
