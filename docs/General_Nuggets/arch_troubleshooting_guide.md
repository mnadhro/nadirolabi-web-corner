---
title: Arch problems + solutions
---
# Bread's list of common Arch problems + solutions


> Intended as a troubleshooting quickstart, or a TL;DR of some ArchWiki sections (a crime, I know) :^)


- ALWAYS read error messages and logs fully. They probably contain the solution to your problem!!
- Remember: there can be unintended consequences to any system changes you make.

[ArchWiki](https://wiki.archlinux.org/ "popup") troubleshooting sections explain everything here in greater depth!

If you are unable to boot:
---

### (a) Can't even get to GRUB

1. [SUPERGRUB](https://www.supergrubdisk.org/super-grub2-disk/) - will detect boot entries and allow you to boot manually Or, boot to the **Arch ISO** , mount partitions, and `arch-chroot /mnt`.
2. If you can't find the issue, reinstall GRUB, and ensure your conguration is updated.
```
grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB
grub-mkconfig -o /boot/grub/grub.cfg
```
3. All else fails? You can try a different [bootloader](https://wiki.archlinux.org/title/Arch_boot_process#Boot_loader), ex. *Refind*. There are some situations where an alternate program may be the most effective solution.

### (b) GRUB shows up, but...

#### Kernel or initramfs is missing?
1. Try regenerating the initramfs: `mkinitcpio -P`. 
   *mkinitcpio* is a Bash script to create an initial ramdisk environment. It is run automatically on every kernel update with a pacman hook.
2. Reinstall: `pacman -S linux linux-firmware` or the kernel you are using.

#### Interrupted mid-upgrade?
> **DO NOT REBOOT!!**

Check `/var/log/pacman.log` and replicate the upgrade exactly.

If a reboot was unavoidable and your system no longer boots, head in with the Arch ISO , mount partitions, `chroot`, and replicate the upgrade exactly.

#### Filesystem not found, or drive is read-only?
1. Boot into the Arch ISO , mount partitions, and `arch-chroot /mnt`
2. Check your fstab! `/etc/fstab`
3. `genfstab -U /mnt >> /mnt/etc/fstab` will generate with UUIDs
4. For read/write issues, "rw,relatime" are set on that partition

#### Filesystem corrupted due to power failure, etc?
Use [fsck](https://wiki.archlinux.org/title/Fsck) to check and repair.

* `fsck -a` will automatically repair.
* If `fsck` cannot find an external journal, umount, write a new journal with `tune2fs -j /dev/partition`, and then run `fsck -p /dev/partition`

### (c) pls help nothing works!!!!!!!

If your partitions are separated, you can easily reinstall your system on your root partition, without touching home.

If they aren't separated, you can still reinstall, but ensure you've backed up all files.

> **!!! ALWAYS ensure you have backed up any important data before clearing or changing partitions !!!**

To save a copy of your currently installed package list:

1. `yay -Qq > packages_list`
2. Reinstall (re-pacstrap, etc) from the [installation guide](https://wiki.archlinux.org/title/Installation_guide)
3. Reinstall **yay/paru**
4. `yay -S $(cat packages_list)`

This is also helpful if you want to set up a new system with the same packages as your current.


Pacman and package issues:
----

#### Recent [news](https://archlinux.org/news/cleaning-up-old-repositories/): update your `/etc/pacman.conf`

Remove all references to [community], [community-testing], [testing], [testing-debug], [staging], and [staging-debug] in your
`/etc/pacman.conf` as these old repositories were recently fully removed.

#### Running out of space on root partition?

Clear your package cache: `sudo pacman -Sc` or `-Scc`

You can also set up pacman hooks to do this automatically.

#### Haven't updated in a while and getting signature errors?

Update the keyring first: `pacman -Sy --needed archlinux-keyring && pacman -Su`

#### Mirror-related errors?

* Re-sync your mirrors with [reflector](https://wiki.archlinux.org/title/Reflector)
* `reflector --latest 10 --sort rate --save /etc/pacman.d/mirrorlist`

If you can't use pacman to get *reflector* due to mirrors not working, download the tar.gz manually, and then use `pacman -
U <file path>`

#### Unable to lock database error

* The lock file prevents two instances of pacman from running at once, but if pacman is interrupted while changing the database, the old file remains.
* `rm /var/lib/pacman/db.lck`

#### Manually reinstall pacman

* Install the statically compiled version [pacman-static](https://aur.archlinux.org/packages/pacman-static)
* Or, boot into the Arch ISO and reinstall




