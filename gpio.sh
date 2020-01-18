source .env
source .gpio_env

# sets the values as defaults if we find none
: ${GPIO:=0}
: ${BASE_GPIO_PATH:=/sys/class/gpio}

printf "GPIO status: %s\n" $GPIO

printf "GPIO path: %s\n" $BASE_GPIO_PATH

# This will terminate all functions if gpio not setup
buckstop(){
    if [ $GPIO -eq 0 ]; then
        exit 0
    fi
}

# Utility function to export a pin if not already exported
exportPin(){
    buckstop;
    if [ ! -e $BASE_GPIO_PATH/gpio$1 ]; then
        echo "$1" > $BASE_GPIO_PATH/export
    fi 
    }
# Utility function to set a pin as an output
setOutput(){ 
    buckstop;
    echo "out" > $BASE_GPIO_PATH/gpio$1/direction;
    }
# Utility function to change state of a light
setLightState(){ 
    buckstop;
    echo $2 > $BASE_GPIO_PATH/gpio$1/value;
    sleep ${3-"0"}
    }

setup(){
    # Export pins so that we can use them
    buckstop;
    exportPin $RED
    exportPin $YELLOW
    exportPin $BLUE
    exportPin $WHITE

    # Set pins as outputs
    setOutput $RED
    setOutput $YELLOW
    setOutput $BLUE
    setOutput $WHITE

    allLightsOff
    }

allLightsOff(){
    buckstop;
    setLightState $RED $OFF
    setLightState $YELLOW $OFF
    setLightState $BLUE $OFF 
    setLightState $WHITE $OFF
    }

shutdown(){
    allLightsOff
    exit 0
}
