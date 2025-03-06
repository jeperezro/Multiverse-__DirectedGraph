from multiverse_project.multiverse.multiverseModel import Multiverse_Model


def main():
    try:
        window = Multiverse_Model()
        window.run()
        
    except KeyboardInterrupt:
        print("Application interrupted by user.")
        
if __name__ == "__main__":
    main()