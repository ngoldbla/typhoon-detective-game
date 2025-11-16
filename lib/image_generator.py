"""Image generation utilities for Typhoon Detective Game"""

from typing import Optional
import requests
import base64
from io import BytesIO
from lib.openai_client import get_openai_client
from lib.database import save_image_data, get_image_data


def generate_case_scene(
    title: str,
    description: str,
    location: str,
    difficulty: str
) -> str:
    """Generate a scene image for a case

    Args:
        title: Case title
        description: Case description
        location: Case location
        difficulty: Case difficulty level

    Returns:
        URL of the generated image
    """
    client = get_openai_client()

    # Create a detailed prompt for the scene
    prompt = f"""Create a dramatic detective game scene illustration in a noir/mystery style.
Scene: {title}
Setting: {location}
Description: {description}

Style: Cinematic, atmospheric, with dramatic lighting and shadows.
Mood: Mystery and intrigue, suitable for a {difficulty} difficulty detective case.
Art style: Semi-realistic digital illustration with strong composition.
No text or labels in the image."""

    try:
        return client.generate_image(
            prompt=prompt,
            model="dall-e-3",
            size="1792x1024",  # Landscape for scene
            quality="standard"
        )
    except Exception as e:
        print(f"Failed to generate case scene: {e}")
        raise


def generate_suspect_portrait(
    name: str,
    description: str,
    alibi: str,
    relationship_to_victim: Optional[str] = None
) -> str:
    """Generate a portrait image for a suspect

    Args:
        name: Suspect name
        description: Physical description and characteristics
        alibi: Suspect's alibi
        relationship_to_victim: How they relate to the victim

    Returns:
        URL of the generated image
    """
    client = get_openai_client()

    # Create a detailed prompt for the portrait
    relationship_text = f"Relationship to victim: {relationship_to_victim}" if relationship_to_victim else ""

    prompt = f"""Create a character portrait for a detective game suspect.
Character: {name}
Description: {description}
{relationship_text}

Style: Professional character portrait, noir detective game aesthetic.
Mood: Mysterious and slightly suspicious, befitting a murder mystery suspect.
Composition: Head and shoulders portrait with neutral background.
Art style: Semi-realistic illustration with good detail and character.
No text or labels in the image."""

    try:
        return client.generate_image(
            prompt=prompt,
            model="dall-e-3",
            size="1024x1024",  # Square for portrait
            quality="standard"
        )
    except Exception as e:
        print(f"Failed to generate suspect portrait: {e}")
        raise


def generate_clue_visualization(
    title: str,
    description: str,
    location_found: str,
    clue_type: Optional[str] = None
) -> str:
    """Generate a visualization for a clue/evidence

    Args:
        title: Clue title
        description: What the clue is
        location_found: Where it was found
        clue_type: Type of evidence (physical, testimonial, etc.)

    Returns:
        URL of the generated image
    """
    client = get_openai_client()

    # Create a detailed prompt for the clue
    type_text = f"Type: {clue_type}" if clue_type else ""

    prompt = f"""Create an illustration of evidence/clue for a detective game.
Evidence: {title}
Description: {description}
Found at: {location_found}
{type_text}

Style: Detailed illustration of the evidence item, detective/crime scene aesthetic.
Composition: Clear view of the evidence, possibly with subtle crime scene context.
Mood: Forensic, investigative, important evidence.
Art style: Semi-realistic, clear and detailed rendering.
No text or labels in the image."""

    try:
        return client.generate_image(
            prompt=prompt,
            model="dall-e-3",
            size="1024x1024",  # Square for evidence
            quality="standard"
        )
    except Exception as e:
        print(f"Failed to generate clue visualization: {e}")
        raise


def generate_location_image(
    location_name: str,
    description: str,
    atmosphere: Optional[str] = None
) -> str:
    """Generate an image of a location

    Args:
        location_name: Name of the location
        description: Description of the location
        atmosphere: Mood/atmosphere of the location

    Returns:
        URL of the generated image
    """
    client = get_openai_client()

    # Create a detailed prompt for the location
    atmosphere_text = f"Atmosphere: {atmosphere}" if atmosphere else "Atmosphere: Mysterious and intriguing"

    prompt = f"""Create a location illustration for a detective game.
Location: {location_name}
Description: {description}
{atmosphere_text}

Style: Atmospheric location shot, noir detective game aesthetic.
Composition: Wide establishing shot showing the location clearly.
Mood: Mystery and intrigue.
Art style: Semi-realistic digital illustration with dramatic lighting.
No text or labels in the image."""

    try:
        return client.generate_image(
            prompt=prompt,
            model="dall-e-3",
            size="1792x1024",  # Landscape for location
            quality="standard"
        )
    except Exception as e:
        print(f"Failed to generate location image: {e}")
        raise


def download_and_store_image(image_url: str, item_type: str, item_id: str) -> bytes:
    """Download an image from URL and store it in the database

    Args:
        image_url: URL of the image to download
        item_type: Type of item ('case', 'clue', or 'suspect')
        item_id: ID of the item

    Returns:
        Binary image data
    """
    try:
        # Download the image
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()

        image_data = response.content

        # Store in database with constructed URL identifier
        url_identifier = f"{item_type}/{item_id}"
        save_image_data(url_identifier, image_data)

        return image_data
    except Exception as e:
        print(f"Failed to download and store image: {e}")
        raise


def get_image_data_uri(image_data: bytes) -> str:
    """Convert binary image data to a data URI for display

    Args:
        image_data: Binary image data

    Returns:
        Data URI string
    """
    if not image_data:
        return ""

    # Encode as base64
    encoded = base64.b64encode(image_data).decode('utf-8')

    # Return as data URI (assuming PNG, could be more sophisticated)
    return f"data:image/png;base64,{encoded}"


def generate_all_case_images(case_data: dict, generate_scene: bool = True) -> dict:
    """Generate all images for a case and store them in the database

    Args:
        case_data: Dictionary containing case information with keys:
            - id, title, description, location, difficulty
            - suspects: list of suspect dicts with 'id' field
            - clues: list of clue dicts with 'id' field
        generate_scene: Whether to generate the main scene image

    Returns:
        Dictionary with image URLs for various case elements
    """
    images = {}

    try:
        # Generate scene image
        if generate_scene:
            print(f"Generating scene image for: {case_data.get('title', 'Unknown Case')}")
            scene_url = generate_case_scene(
                title=case_data['title'],
                description=case_data['description'],
                location=case_data['location'],
                difficulty=case_data.get('difficulty', 'Medium')
            )
            images['scene'] = scene_url

            # Download and store the image
            try:
                download_and_store_image(scene_url, 'case', case_data['id'])
            except Exception as e:
                print(f"Failed to download scene image: {e}")

        # Generate suspect portraits
        images['suspects'] = []
        for i, suspect in enumerate(case_data.get('suspects', [])):
            print(f"Generating portrait for suspect {i+1}/{len(case_data.get('suspects', []))}: {suspect.get('name', 'Unknown')}")
            try:
                portrait_url = generate_suspect_portrait(
                    name=suspect['name'],
                    description=suspect['description'],
                    alibi=suspect.get('alibi', ''),
                    relationship_to_victim=suspect.get('relationshipToVictim')
                )
                images['suspects'].append(portrait_url)

                # Download and store the image
                try:
                    download_and_store_image(portrait_url, 'suspect', suspect['id'])
                except Exception as e:
                    print(f"Failed to download portrait for {suspect.get('name')}: {e}")

            except Exception as e:
                print(f"Failed to generate portrait for {suspect.get('name')}: {e}")
                images['suspects'].append(None)

        # Generate clue visualizations
        images['clues'] = []
        for i, clue in enumerate(case_data.get('clues', [])):
            print(f"Generating visualization for clue {i+1}/{len(case_data.get('clues', []))}: {clue.get('title', 'Unknown')}")
            try:
                clue_url = generate_clue_visualization(
                    title=clue['title'],
                    description=clue['description'],
                    location_found=clue.get('location', 'Unknown location')
                )
                images['clues'].append(clue_url)

                # Download and store the image
                try:
                    download_and_store_image(clue_url, 'clue', clue['id'])
                except Exception as e:
                    print(f"Failed to download clue image for {clue.get('title')}: {e}")

            except Exception as e:
                print(f"Failed to generate visualization for {clue.get('title')}: {e}")
                images['clues'].append(None)

        return images

    except Exception as e:
        print(f"Error generating case images: {e}")
        raise
