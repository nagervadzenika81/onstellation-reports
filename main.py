from flask import Flask, request, send_file, jsonify
import matplotlib.pyplot as plt
import numpy as np
from skyfield.api import Topos, load
from skyfield.data import hipparcos
import os

app = Flask(__name__)
@app.route('/')
def home():
    return "Constellation Report API is running!"


# Load astronomical data
ts = load.timescale()
eph = load('de421.bsp')
earth = eph['earth']

# Load star catalog (Hipparcos)
with load.open(hipparcos.URL) as f:
    stars = hipparcos.load_dataframe(f)

def generate_constellation_report(date, latitude, longitude, custom_label=None):
    """Generates a constellation report as an image."""
    
    # Convert input date to Skyfield format
    time = ts.utc(*map(int, date.replace(":", "-").replace(" ", "-").split("-")))

    # Observer's location
    location = Topos(latitude_degrees=latitude, longitude_degrees=longitude)
    observer = (earth + location).at(time)

    # Compute star positions
    astro = observer.observe(stars)
    alt, az, distance = astro.apparent().altaz()

    # Filter visible stars
    visible_stars = stars[alt.degrees > 0]

    # Plot settings
    fig, ax = plt.subplots(figsize=(10, 10), dpi=300)
    ax.set_xlim(0, 360)
    ax.set_ylim(0, 90)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)

    # Background color
    ax.set_facecolor("#000016")
    star_color = "white"
    constellation_color = "gold"

    # Plot stars
    ax.scatter(az.degrees, alt.degrees, s=2, c=star_color, alpha=0.8)

    # Plot constellations (random sample)
    for _ in range(10):
        i, j = np.random.randint(0, len(visible_stars), 2)
        ax.plot([az.degrees[i], az.degrees[j]], [alt.degrees[i], alt.degrees[j]], color=constellation_color, alpha=0.5)

    # Add custom label
    if custom_label:
        ax.set_title(custom_label, color=star_color, fontsize=14, fontweight="bold")

    # Save image
    file_path = "constellation_report.png"
    plt.savefig(file_path, bbox_inches="tight", dpi=300)
    plt.close()
    
    return file_path

@app.route('/generate_report', methods=['POST'])
def generate_report():
    """API Endpoint to generate a constellation report"""
    data = request.json
    date = data.get("date", "2025-03-01 22:00:00")
    latitude = float(data.get("latitude", 41.64))
    longitude = float(data.get("longitude", 41.63))
    custom_label = data.get("custom_label", "Your Night Sky")

    file_path = generate_constellation_report(date, latitude, longitude, custom_label)

    return send_file(file_path, mimetype='image/png')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)

    import os


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)  # Use port 10000 (matches Render logs)
    import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Default to 10000
    app.run(host="0.0.0.0", port=port)


