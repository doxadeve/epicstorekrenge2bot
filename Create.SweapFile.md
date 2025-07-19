# remove previus swap file

1) sudo swapoff /swapfile
2) sudo rm /swapfile

============°°°°===========°°°°°°==========
# Create a 1GB swap file
3) sudo fallocate -l 1G /swapfile  

# Set the correct permissions
4) sudo chmod 600 /swapfile       

5) sudo mkswap /swapfile

# Enable the Swap File: Activate the swap space:

6) sudo swapon /swapfile

# Make It Persistent: Add the following line to /etc/fstab to ensure the swap file is enabled after reboot:

7) echo '/swapfile swap swap defaults 0 0' | sudo tee -a /etc/fstab

#Verify the Swap File Run the following command to confirm the swap file is active:

8) sudo swapon --show

#Done✅


# Extra 👇

============°°°°===========°°°°°°==========
You should see an entry for /swapfile. Additionally, check overall system memory and swap usage:

free -h


=============°°°°===========°°°°°°==========
# Troubleshooting

# Issue persists after formatting: Ensure you have sufficient disk space for the swap file. Check available space:

df -h

============°°°°===========°°°°°°==========
# Alternative method to create a swap file: Use dd instead of fallocate if fallocate has issues:

sudo dd if=/dev/zero of=/swapfile bs=1M count=1024
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile