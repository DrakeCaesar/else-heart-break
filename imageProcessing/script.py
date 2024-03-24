from PIL import Image
import numpy as np

def remove_similar_rows_and_columns(image_path, output_path, similarity_threshold=0.99):
    # Load the image
    img = Image.open(image_path)
    # Convert the image to a numpy array
    data = np.array(img)

    # Determine which rows to keep
    rows_to_keep = [True]  # Always keep the first row
    for i in range(1, data.shape[0]):
        # Calculate similarity with the previous row
        similarity = np.mean(data[i] == data[i-1])
        # If similarity is less than the threshold, keep the row
        if similarity < similarity_threshold:
            rows_to_keep.append(True)
        else:
            rows_to_keep.append(False)

    # Determine which columns to keep
    columns_to_keep = [True]  # Always keep the first column
    for i in range(1, data.shape[1]):
        # Calculate similarity with the previous column
        similarity = np.mean(data[:, i] == data[:, i-1])
        # If similarity is less than the threshold, keep the column
        if similarity < similarity_threshold:
            columns_to_keep.append(True)
        else:
            columns_to_keep.append(False)

    # Filter the data to remove similar rows and columns
    filtered_data = data[rows_to_keep, :][:, columns_to_keep]

    # Create a new image from the filtered data
    new_img = Image.fromarray(filtered_data)
    # Save the new image
    new_img.save(output_path)
    
def generate_similarity_mask(image_path, mask_path, similarity_threshold=0.95):
    # Assume the image has already been processed and saved to image_path
    # Load the processed image
    img = Image.open(image_path)
    data = np.array(img)

    # Initialize mask with zeros (black)
    mask = np.zeros_like(data, dtype=np.uint8)

    # Check for row similarity
    for i in range(1, data.shape[0]):
        row_similarity = (data[i] == data[i-1]).all(axis=-1)
        mask[i][row_similarity] = 255  # Set to white where similar

    # Check for column similarity
    for i in range(1, data.shape[1]):
        col_similarity = (data[:, i] == data[:, i-1]).all(axis=-1)
        mask[:, i][col_similarity] = 255  # Set to white where similar

    # Save the mask
    Image.fromarray(mask).save(mask_path)

# Path to the input and output images
input_path = 'input.png'
output_path = 'output.png'

# Call the function
remove_similar_rows_and_columns(input_path, output_path)

# Path to the processed image and the mask image
processed_image_path = 'output.png'
mask_path = 'mask.png'

# Generate the mask
generate_similarity_mask(processed_image_path, mask_path)
