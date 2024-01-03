from ble import BLE_lantern_control
from threading import Thread
from time import sleep

def control_thread(lantern_control):
    while True:
        if not lantern_control.is_connected():
            print("***Lantern disconnected. Closing...")
            break

        rgb_input = input("Enter RGB values (R G B) or q to quit: ")
        lantern_control.push_queue(rgb_input)

        if rgb_input == "q":
            print("***Lantern disconnected. Closing...")
            break

def main():
    lantern_control = BLE_lantern_control()

    # Connect to lantern and wait until connected.
    Thread(target=lantern_control.connect, args=()).start()

    # Wait until a max time is reached.
    print("Connecting to lantern...")
    total_wait_time_max = 20
    current_wait_time = 0
    wait_time_increment = 1
    while not lantern_control.is_connected():
        if current_wait_time >= total_wait_time_max:
            print(f"Connection took too long with {current_wait_time} seconds. Exiting...")
            return
        current_wait_time += wait_time_increment
        sleep(wait_time_increment)
    print("Connected!")

    # Start color control.
    Thread(target=control_thread, args=(lantern_control,)).start()

if __name__ == "__main__":
    main()
