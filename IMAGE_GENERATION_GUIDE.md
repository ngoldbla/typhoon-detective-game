# Image Generation Guide for Typhoon Detective Game

This guide explains how to integrate OpenAI's DALL-E image generation API to create visuals that enhance the detective game experience.

## Overview

OpenAI's DALL-E API (accessed via the `images.generate` endpoint) can generate:
- Case scene illustrations
- Suspect portraits
- Clue visualizations
- Location/environment images
- Evidence photos

## API Integration

### 1. Update OpenAI Client

Add image generation capability to `lib/openai_client.py`:

```python
def generate_image(
    self,
    prompt: str,
    size: str = "1024x1024",
    quality: str = "standard",
    n: int = 1
) -> str:
    """Generate image using DALL-E

    Args:
        prompt: Description of the image to generate
        size: Image size - "1024x1024", "1792x1024", or "1024x1792"
        quality: "standard" or "hd" (hd costs more)
        n: Number of images to generate (1-10)

    Returns:
        URL of the generated image
    """
    try:
        response = self.client.images.generate(
            model="dall-e-3",  # or "dall-e-2" for lower cost
            prompt=prompt,
            size=size,
            quality=quality,
            n=n
        )

        return response.data[0].url

    except Exception as e:
        error_str = str(e)
        print(f"Error generating image: {error_str}")
        raise Exception(f"Image generation error: {error_str}") from e
```

### 2. Helper Function

Add a module for image generation helpers (`lib/image_generator.py`):

```python
"""Image generation utilities for detective cases"""

from typing import Optional
from .openai_client import get_openai_client


def generate_case_scene(case_title: str, case_description: str, location: str) -> str:
    """Generate a scene image for a detective case

    Args:
        case_title: Title of the case
        case_description: Description of the case
        location: Location where the case takes place

    Returns:
        URL of the generated image
    """
    prompt = f"""Create a child-friendly, cartoon-style illustration of a detective mystery scene.

    Scene: {case_title}
    Description: {case_description}
    Location: {location}

    Style: Colorful, comic book style, suitable for children ages 7+, non-scary, whimsical.
    No text in the image.
    """

    client = get_openai_client()
    return client.generate_image(prompt, size="1792x1024", quality="standard")


def generate_suspect_portrait(suspect_name: str, suspect_description: str) -> str:
    """Generate a portrait of a suspect

    Args:
        suspect_name: Name of the suspect
        suspect_description: Physical description of the suspect

    Returns:
        URL of the generated image
    """
    prompt = f"""Create a child-friendly cartoon character portrait.

    Character: {suspect_name}
    Description: {suspect_description}

    Style: Friendly cartoon style, colorful, expressive face, suitable for children ages 7+.
    Portrait should be from chest up, clear facial features.
    No text in the image.
    """

    client = get_openai_client()
    return client.generate_image(prompt, size="1024x1024", quality="standard")


def generate_clue_visualization(clue_title: str, clue_description: str) -> str:
    """Generate a visualization of a clue

    Args:
        clue_title: Title of the clue
        clue_description: Description of the clue

    Returns:
        URL of the generated image
    """
    prompt = f"""Create a child-friendly illustration of a detective clue or evidence.

    Clue: {clue_title}
    Details: {clue_description}

    Style: Clear, detailed, cartoon-style illustration, colorful, suitable for children ages 7+.
    Focus on the object/clue itself.
    No text in the image.
    """

    client = get_openai_client()
    return client.generate_image(prompt, size="1024x1024", quality="standard")


def generate_location_image(location_name: str, location_type: str) -> str:
    """Generate an image of a location

    Args:
        location_name: Name of the location
        location_type: Type of location (e.g., "school", "park", "library")

    Returns:
        URL of the generated image
    """
    prompt = f"""Create a child-friendly cartoon illustration of a location.

    Location: {location_name}
    Type: {location_type}

    Style: Colorful, inviting cartoon style, suitable for children ages 7+, daytime scene.
    Show the exterior or interior of the location clearly.
    No text in the image.
    """

    client = get_openai_client()
    return client.generate_image(prompt, size="1792x1024", quality="standard")
```

## Implementation Strategies

### Option 1: Generate Images During Case Creation

Modify `lib/case_generator.py` to include image generation:

```python
def generate_case(difficulty, theme, location, custom_scenario=None, generate_images=False):
    """Generate a new detective case

    Args:
        difficulty: Case difficulty level
        theme: Case theme
        location: Case location
        custom_scenario: Optional custom scenario
        generate_images: Whether to generate images for the case

    Returns:
        Complete case with optional images
    """
    # ... existing case generation logic ...

    if generate_images:
        try:
            # Generate case scene
            case['scene_image'] = generate_case_scene(
                case['title'],
                case['description'],
                case['location']
            )

            # Generate suspect portraits
            for suspect in case['suspects']:
                suspect['portrait_url'] = generate_suspect_portrait(
                    suspect['name'],
                    suspect['description']
                )

            # Generate clue visualizations
            for clue in case['clues']:
                clue['image_url'] = generate_clue_visualization(
                    clue['title'],
                    clue['description']
                )

        except Exception as e:
            print(f"Warning: Image generation failed: {e}")
            # Continue without images

    return case
```

### Option 2: Generate Images On-Demand

Generate images only when the user requests them (saves cost):

```python
# In pages/3_🔍_Case_Details.py

if st.button("🎨 Generate Scene Image"):
    with st.spinner("Creating scene image..."):
        try:
            scene_image = generate_case_scene(
                case['title'],
                case['description'],
                case['location']
            )
            case['scene_image'] = scene_image
            st.session_state.cases = st.session_state.cases  # Trigger update
            st.rerun()
        except Exception as e:
            st.error(f"Failed to generate image: {e}")

# Display image if it exists
if 'scene_image' in case and case['scene_image']:
    st.image(case['scene_image'], use_column_width=True)
```

### Option 3: Batch Generation with Caching

Generate images in batches and cache them:

```python
import hashlib
import os
from pathlib import Path

def get_image_cache_path(prompt: str) -> str:
    """Get cache file path for an image prompt"""
    cache_dir = Path(".image_cache")
    cache_dir.mkdir(exist_ok=True)

    # Create hash of prompt for filename
    prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
    return cache_dir / f"{prompt_hash}.png"

def generate_or_get_cached_image(prompt: str, **kwargs) -> str:
    """Generate image or return cached version"""
    cache_path = get_image_cache_path(prompt)

    if cache_path.exists():
        # Return local cached image
        return str(cache_path)

    # Generate new image
    client = get_openai_client()
    image_url = client.generate_image(prompt, **kwargs)

    # Download and cache
    import requests
    response = requests.get(image_url)
    cache_path.write_bytes(response.content)

    return str(cache_path)
```

## UI Integration Examples

### Display Case Scene in Case Details

```python
# In pages/3_🔍_Case_Details.py

st.markdown(f"## {case['title']}")

# Display scene image if available
if 'scene_image' in case and case['scene_image']:
    st.image(case['scene_image'], caption=f"Crime Scene: {case['location']}", use_column_width=True)
else:
    # Option to generate image
    if st.button("🎨 Generate Scene Image", key="gen_scene"):
        with st.spinner("Creating scene illustration..."):
            try:
                scene_image = generate_case_scene(
                    case['title'],
                    case['description'],
                    case['location']
                )
                case['scene_image'] = scene_image
                st.rerun()
            except Exception as e:
                st.error(f"Failed to generate image: {e}")
```

### Display Suspect Portraits

```python
# In the Suspects tab

for suspect in case['suspects']:
    col1, col2 = st.columns([1, 3])

    with col1:
        # Show portrait if available
        if 'portrait_url' in suspect and suspect['portrait_url']:
            st.image(suspect['portrait_url'], width=150)
        else:
            # Placeholder or generate button
            if st.button(f"🎨 Generate Portrait", key=f"gen_portrait_{suspect['id']}"):
                with st.spinner(f"Creating portrait of {suspect['name']}..."):
                    try:
                        portrait = generate_suspect_portrait(
                            suspect['name'],
                            suspect['description']
                        )
                        suspect['portrait_url'] = portrait
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to generate portrait: {e}")

    with col2:
        st.markdown(f"### {suspect['name']}")
        st.markdown(suspect['description'])
```

### Display Clue Images

```python
# In the Clues tab

for clue in case['clues']:
    with st.expander(f"{clue['emoji']} {clue['title']}"):
        # Show image if available
        if 'image_url' in clue and clue['image_url']:
            st.image(clue['image_url'], caption=clue['title'], use_column_width=True)

        st.markdown(f"**Location:** {clue['location']}")
        st.markdown(f"**Type:** {clue['type']}")
        st.markdown(clue['description'])

        # Option to generate image
        if 'image_url' not in clue or not clue['image_url']:
            if st.button(f"🎨 Visualize Clue", key=f"gen_clue_{clue['id']}"):
                with st.spinner("Creating clue visualization..."):
                    try:
                        image_url = generate_clue_visualization(
                            clue['title'],
                            clue['description']
                        )
                        clue['image_url'] = image_url
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to generate image: {e}")
```

## Cost Considerations

### DALL-E Pricing (as of 2025)

- **DALL-E 3**:
  - Standard quality: ~$0.040 per image (1024x1024)
  - HD quality: ~$0.080 per image (1024x1024)
  - Standard quality: ~$0.080 per image (1792x1024 or 1024x1792)

- **DALL-E 2** (lower cost option):
  - ~$0.020 per image (1024x1024)

### Cost Estimation

For a typical case with images:
- 1 scene image (1792x1024): $0.08
- 3-5 suspect portraits (1024x1024): $0.12-$0.20
- 4-6 clue images (1024x1024): $0.16-$0.24

**Total per case: ~$0.36-$0.52**

### Cost Optimization Strategies

1. **On-demand generation**: Only generate images when users click a button
2. **Image caching**: Cache generated images to avoid regenerating similar content
3. **Use DALL-E 2**: For lower-priority images, use DALL-E 2 ($0.02 vs $0.04)
4. **Standard quality**: Use standard quality instead of HD for most images
5. **Optional feature**: Make image generation an optional premium feature
6. **Batch generation**: Generate multiple images in one session to amortize costs

## Best Practices

### Prompt Engineering for Child-Friendly Images

Always include in prompts:
- "child-friendly"
- "cartoon style" or "comic book style"
- "suitable for ages 7+"
- "colorful" and "whimsical"
- "non-scary"
- "no text in the image" (text often comes out garbled)

### Example Prompts

**Good prompt:**
```
Create a child-friendly cartoon illustration of a school library.
Style: Colorful, inviting, suitable for ages 7+, daytime scene with warm lighting.
Show bookshelves, reading tables, and a cozy atmosphere.
No text in the image.
```

**Poor prompt:**
```
A dark mysterious library at night
```

### Error Handling

Always wrap image generation in try-catch blocks:

```python
try:
    image_url = generate_image(prompt)
    case['image_url'] = image_url
except Exception as e:
    st.warning(f"Could not generate image: {e}")
    # Continue without image - don't break the user experience
```

### User Settings

Add a setting to enable/disable automatic image generation:

```python
# In streamlit_app.py sidebar
if 'auto_generate_images' not in st.session_state:
    st.session_state.auto_generate_images = False

st.session_state.auto_generate_images = st.checkbox(
    "Auto-generate images",
    value=st.session_state.auto_generate_images,
    help="Automatically generate images for new cases (uses API credits)"
)
```

## Implementation Checklist

- [ ] Add `generate_image()` method to `lib/openai_client.py`
- [ ] Create `lib/image_generator.py` with helper functions
- [ ] Update `lib/case_generator.py` to optionally generate images
- [ ] Add image generation buttons to Case Details page
- [ ] Add image display logic to Case Details page
- [ ] Implement image caching (optional but recommended)
- [ ] Add user setting to enable/disable auto-generation
- [ ] Update case data structure to include image URLs
- [ ] Add error handling for failed image generation
- [ ] Test with various case types and themes
- [ ] Document image generation costs for users

## Security Considerations

1. **Content Safety**: DALL-E has built-in content filters for inappropriate content
2. **Rate Limiting**: Implement rate limiting to prevent API abuse
3. **Cost Limits**: Set spending limits on your OpenAI account
4. **Image Storage**: Consider privacy when storing/caching generated images

## Future Enhancements

1. **Custom art styles**: Let users choose between different art styles
2. **Image variations**: Generate multiple versions and let users pick
3. **Animation**: Use image sequences to create simple animations
4. **Image editing**: Allow users to request edits to generated images
5. **Gallery**: Create a gallery of all generated images for a case
6. **Download**: Let users download generated images
7. **Social sharing**: Share cases with generated images

## Additional Resources

- [OpenAI DALL-E API Documentation](https://platform.openai.com/docs/guides/images)
- [DALL-E Prompt Engineering Guide](https://platform.openai.com/docs/guides/images/prompting)
- [OpenAI Pricing](https://openai.com/pricing)
