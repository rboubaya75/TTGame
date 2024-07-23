import matplotlib.pyplot as plt
import numpy as np

def generate_table_image():
    fig, ax = plt.subplots(figsize=(8, 4))

    # Draw table
    ax.add_patch(plt.Rectangle((0, 0), 8, 4, color='#006400'))  # Dark green table

    # Draw middle line
    ax.plot([4, 4], [0, 4], color='white', linewidth=2)

    # Draw horizontal lines
    ax.plot([0, 8], [2, 2], color='white', linewidth=2)

    # Draw border lines
    ax.plot([0, 0], [0, 4], color='white', linewidth=2)
    ax.plot([8, 8], [0, 4], color='white', linewidth=2)
    ax.plot([0, 8], [0, 0], color='white', linewidth=2)
    ax.plot([0, 8], [4, 4], color='white', linewidth=2)

    ax.set_xlim([0, 8])
    ax.set_ylim([0, 4])
    ax.axis('off')

    plt.savefig("C:\\Users\\RachidBOUBAYA\\TTGAME\\table_image.png", bbox_inches='tight', pad_inches=0)
    plt.close()

generate_table_image()
