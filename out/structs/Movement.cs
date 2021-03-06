package lostsouls.net.lostsocket.lostsouls.net.kumo.structs;
import java.util.ArrayList;
import java.util.TreeMap;
import net.kaminari.Packet;
import net.kaminari.PacketReader;
import net.kaminari.Optional;
import net.kaminari.IMarshal;
import net.kaminari.packers.IData;
import net.kaminari.packers.IHasId;
import net.kaminari.packers.IHasDataVector;
public class Movement implements IData
{
    public void pack(IMarshal marshal, Packet packet)
    {
        packet.getData().write((char)this.direction);
    }
    public bool unpack(IMarshal marshal, PacketReader packet)
    {
        if (packet.bytesRead() + this.size(marshal) > packet.bufferSize())
        {
            return false;
        }
        this.direction = packet.getData().readchar();
        return true;
    }
    public int size(IMarshal marshal)
    {
        int size = 0;
        size += marshal.size(char.class);
        return size;
    }
    public char direction;
}

