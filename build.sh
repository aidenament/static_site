python3 src/main.py "/"

# Ensure CNAME file is copied to the build output
cp CNAME docs/ || echo "No CNAME file found"