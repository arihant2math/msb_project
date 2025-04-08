from ultralytics import FastSAM

# Create a FastSAM model
model = FastSAM('FastSAM-x.pt')  # or FastSAM-x.pt

# Track with a FastSAM model on a video
results = model.track(source="data/ikea/20240507_175647.ts",
                      save=True)
