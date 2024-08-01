---
layout: default
parent: "Guides"
title: "Identify the C0-microSD"
nav_order: 1
---

<script src="/assets/js/tabs.js"></script>

# Identify the Signaloid C0-microSD

<ol>
  <li>
    Insert the Signaloid C0-microSD into your computer. The device should present itself as a 20.2 MB (19.3 MiB) unformatted block storage device. Depending on your OS, you might be prompted to format the device. Do not format the device; instead ignore any prompt. In Figure 1, you can find an example of the pop-up message you might see in macOS:

    <div style="max-width: 360px; margin-left: auto; margin-right: auto; margin-top: 16px">
      <table style = "text-align: center;">
        <tr>
            <td><img src="/assets/images/mac-popup-dark.png" alt="mac popup"/></td>
        </tr>
        <tr>
            <td><b>Figure 1:</b> Pop-up message in macOS when inserting the C0-microSD.</td>
        </tr>
      </table>
    </div>
  </li>

  <li>
    Verify the device path at which the Signaloid C0-microSD device shows up in your operating system. Following is a list of examples on different operating systems.
  </li>
</ol>



{% tabs log%}

{% tab log mac %}
  On macOS, you can run `diskutil list`

  ```
  % diskutil list

  ...
  /dev/disk4 (internal, physical):
  #:                       TYPE NAME                    SIZE       IDENTIFIER
  0:                                                   *20.2 MB    disk4
  ```

  In this example, the Signaloid C0-microSD device is located in `/dev/disk4`.
{% endtab %}


{% tab log linux %}
  On Linux, you can run `lsblk`

  ```
  % lsblk

  NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
  sda      8:0    0    64G  0 disk 
  ├─sda1   8:1    0     1G  0 part /boot/efi
  └─sda2   8:2    0  62.9G  0 part /
  sdb      8:16   1  19.3M  0 disk 
  sr0     11:0    1  1024M  0 rom  
  ```

  In this example, the Signaloid C0-microSD device is located in `/dev/sdb`.
{% endtab %}


{% tab log windows %}
  On Windows, you can run `diskpart` followed by `list disk` and `exit`

```
% diskpart

DISKPART> list disk

  Disk ###  Status         Size     Free     Dyn  Gpt
  --------  -------------  -------  -------  ---  ---
  Disk 0    Online          256 GB      0 B        *
  Disk 1    Online           19 MB      0 B

DISKPART> exit
```

On Windows, raw disk devices can be accessed via a special path format: `\\.\PhysicalDriveN`, where `N` is the disk number. In this example, the C0-microSD is `Disk 1`, and its path is `\\.\PhysicalDrive1`.
{% endtab %}

{% endtabs %}

