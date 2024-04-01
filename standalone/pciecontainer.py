from prettytable import PrettyTable
from enum import Enum
import pickle
from arrowlake.pcie_utils.pcie_h import *
import bitstruct

class pciecontainer(object):
    def __init__(self, pcie_xbar =  0xC0000000, reg_bar = 0xE0000000):
        print('PCIe Utilities Container...')
        self.pcie_mmio_xbar       = pcie_xbar
        self.pcie_mmio2sb_regbar  = reg_bar
        self.root_ports           = [0x100, 0x600,0x061,0x62,0x64]
        #self.rp_bdf               = self.get_rp_bdf()
        self.itp_halt()
        self.debug = 0
    
    def cfg_read(self, bus = 0, device = 0, function = 0, offset = 0, access = 'mmio', port_id = 0, seg_id =0, size = 4):
        if (self.debug):
            print('Configuration Read : Bus : {0}, Dev : {1}, Fun : {2}, Offset : {3}'.format(bus, device, function, offset))
        if (access == 'mmio'):
            return self.cfg_read_mmio(bus,device,function,offset, size)
        else:
            return self.cfg_read_sb(port_id, seg_id, offset, size)
    
    def cfg_read_mmio(self, bus = 0, device = 0, function = 0, offset = 0, size = 4):
        addr = self.get_pcie_mmio_addr(bus, device,function,offset)
        if(size == 4):
            return self.read_dword(addr)
        elif (size == 2):
            return self.read_word(addr)
        elif (size == 1):
            return self.read_byte(addr)

    def cfg_read_sb(self, port_id = 0, seg_id = 0, offset = 0, size = 4 ):
        addr = self.get_pcie_sb_addr(port_id, seg_id, offset)
        if(size == 4):
            return self.read_dword(addr)
        elif (size == 2):
            return self.read_word(addr)
        elif (size == 1):
            return self.read_byte(addr)

    def read_byte(self, addr = 0):
        return mem(addr, 1)

    def read_word(self, addr = 0):
        return mem(addr, 2)

    def read_dword(self, addr = 0):
        return mem(addr, 4)
    
    def read_quadword(self, addr = 0):
        return mem(addr, 8)

    def write_byte(self, addr = 0, data = 0):
        return mem(addr, 1, data)

    def write_word(self, addr = 0):
        return mem(addr, 2, data)

    def write_dword(self, addr = 0):
        return mem(addr, 4, data)
    
    def write_quadword(self, addr = 0):
        return mem(addr, 8, data)

    def cfg_write(self, bus = 0, device = 0, function = 0, offset = 0, access = 'mem' ):
        print('Configuration Write : Bus : {0}, Dev : {1}, Fun : {2}, Offset : {3}, Data : {4}'.format(bus, device, function, offset, data))

    def mem_read(self, bus = 0, device = 0, function = 0, offset = 0 ):
        print('Memory Read')

    def mem_write(self, bus = 0, device = 0, function = 0, offset = 0 ):
        print('Memory Write')
    
    def get_pcie_mmio_addr(self, bus = 0, device = 0, function = 0, offset = 0 ):
        return self.pcie_mmio_xbar + ( bus << 20 ) + ( device << 15 ) + ( function<< 12 ) + offset

    def get_pcie_sb_addr(self, die = 'soc', port_id = 0, segment_id = 0, offset = 0 ):
        print('Get SB Address')
        if (die == 'soc'):
            selfp2sb_regbar = 'soc.south.p2sb.cfg.sbreg_bar.rba'
        else:
            print('only for Soc Die is implemented...')
        return self.pcie_mmio2sb_regbar + (port_id<<16) + offset
        
    def itp_halt(self):
        itp.halt()

    def cfg_space_dump(self, bus = 0, device = 0, function = 0, file_path = 0):
        addr      = self.get_pcie_mmio_addr(bus,device,function)
        cfg_space = memblock(addr,4,1024)
        if (file_path == 0):
            file_path = 'c:\\bdf_{0}_{1}_{2}'.format(bus,device,function)
        with open(file_path,'wb') as fp:
            pickle.dump(cfg_space, fp)
        return cfg_space
        
    def cfg_space_load(self, file_path = 0):
        if (file_path == 0):
            file_path = 'c:\\bdf_{0}_{1}_{2}'.format(0, 0, 0)
        with open(file_path,'rb') as fp:
            cfg_space = pickle.load(fp)
        return cfg_space

    def check_port_detect(self, bus = 0, device = 0, function = 0):

        did = self.cfg_read(bus, device, function, offset = 0)
        if (did == 0xFFFFFFFF):
            return False
        else:
            return True
        
    def get_did(self, bus = 0, device = 0, function = 0):

        return self.cfg_read(bus, device, function, offset = 0)

    def get_ddid(self, bus = 0, device = 0, function = 0):

        sbus = self.get_secbus_num(bus, device, function)
        if(sbus == 0):
            return None
        else:
            did = self.get_did(sbus) == 0xFFFFFFFF
            if(did):
                return None
            else:
                return hex(self.get_did(bus = sbus))
        
        
    def get_header_type(self, bus = 0, device = 0, function = 0):

        [multi_fun, header_type ] = bitstruct.unpack('u1u7', self.cfg_read(bus, device, function, offset = 0xE, size = 1).to_bytes(1,'big'))

        return [multi_fun,header_type]

    def get_port_type(self, bus = 0, device = 0, function = 0):
        port_type_offset         = 2
        exp_cap_offset           = self.get_cap_offset(bus, device, function, cap_id_exp = 0x10)
        if(exp_cap_offset == 0):
            return None
            
        exp_cap_offset_port_type = exp_cap_offset + port_type_offset

        [port_type, b] = bitstruct.unpack('u4u4', self.cfg_read(bus, device, function, exp_cap_offset_port_type, size = 1).to_bytes(1,'big'))
        if(port_type == 0x9):
            port = 'RPiEP'
        elif (port_type ==  0x4):
            port = 'RP'
        elif (port_type ==  0x0):
            port = 'EP'
        elif (port_type ==  0x1):
            port = 'Legacy EP'
        else:
            port = port_type

        return port

    def get_secbus_num(self, bus = 0, device = 0, function = 0):
        return self.cfg_read(bus, device, function, offset = 0x19, size = 1)

    def scan_bus(self, bus_num = 256, dev_num = 32, fun_num = 8):
        field_names          = ['Port' , 'Primary Bus',
                                'Device', 'Function',
                                'DeviceId', 'secondary Bus',
                                'Device Connected']
        pcie_ports              = PrettyTable()
        pcie_ports.title        = "Scan all PCIe Ports"
        pcie_ports.field_names  = field_names
        
        for bus in range(bus_num):
            for device in range(dev_num):
                for function in range(fun_num):
                    if(not self.check_port_detect(bus, device, function)):
                        continue
                    port = self.get_port_type(bus, device, function)
                    if (port == 'RP' or port == 'EP'):
                        ddid = self.get_ddid(bus, device, function)
                        
                        pcie_ports.add_row([ port, bus, device, function,
                                             hex(self.get_did(bus, device, function)),
                                             hex(self.get_secbus_num(bus, device, function)),
                                             ddid])
                        #print('Bus {0}, device {1}, function {2}, did {3}'.format(bus,device,function,hex(did)))
        print(pcie_ports)

    def print_Capabilities(self, bus = 0, device = 0, function = 0):
        field_names          = ['parameter' , 'RP Support', 'EP Support', 'RP Current Value', 'EP Current Value']
        cfg_cap              = PrettyTable()
        cfg_cap.title        = "Root Port and End Point Capabilitiy and Negotiated"
        cfg_cap.field_names  = field_names
        cfg_cap.add_row([ "Link Device State",'-', '-', '-', '-'])
        cfg_cap.add_row([ "Link Link State",'-', '-', '-', '-', '-'])
        cfg_cap.add_row([ "Link State",'-', '-', '-', '-', '-'])
        cfg_cap.add_row([ "Link Speed",'-', '-', '-', '-', '-'])
        cfg_cap.add_row([ "Link Width",'-', '-', '-', '-', '-'])
        cfg_cap.add_row([ "Link Max Payload Size",'-', '-', '-', '-', '-'])
        cfg_cap.add_row([ "Link PCIe L0s",'-', '-', '-', '-', '-'])
        cfg_cap.add_row([ "Link PCIe ASPM L1",'-', '-', '-', '-', '-'])
        cfg_cap.add_row([ "Link PCIe PCIPM L1 (D3Hot)",'-', '-', '-', '-', '-'])
        cfg_cap.add_row([ "Link PCIe L1.1",'-', '-', '-', '-', '-'])
        cfg_cap.add_row([ "Link PCIe L1.2",'-', '-', '-', '-', '-'])
        cfg_cap.add_row([ "Bar0",'-', '-', '-', '-', '-'])
        cfg_cap.add_row([ "Bar1",'-', '-', '-', '-', '-'])

    def set_linkwidth(self, bus = 0, device = 0, function = 0, linkwidth = 1):
        print('''This function set Linkwidth''')

    def set_mps(self, bus = 0, device = 0, function = 0, mps = 256):
        print('''This function set Max Payload Size''')

    def set_d3hot(self, bus = 0, device = 0, function = 0):
        print('''This function set d3hot''')
        pwr_mgnt_control_reg_off = self.get_offset(PCIE_STD_CAP_PTR, pcie_std_capability_ids().PCI_CAP_ID_PM)
        add = 0xC0000000 + ( bus << 20 ) + ( device << 15 ) + ( function<< 12 ) + pwr_mgnt_control_reg_off
        val = mem(add+4,4) + PWR_STATE['D3HOT']        
        mem(add+4, 4, val)

    def set_d3cold(self, bus = 0, device = 0, function = 0):
        print('''This function set Linkwidth''')

    def set_l1ss(self, bus, device, function):
            [a,b,c,d,self.l1ss_supported, self.aspm_L11_supported, self.aspm_L12_supported, self.pcipm_L11_supported, self.pcipm_L12_supported] = bitstruct.unpack('u8u8u8u3u1u1u1u1u1',nvme_config_space[int(self.l1ss_cap/4)].to_bytes(4,'big'))
            [a,b,c,d,self.aspm_L11_enable, self.aspm_L12_enable, self.pcipm_L11_enable, self.pcipm_L12_enable] = bitstruct.unpack('u8u8u8u4u1u1u1u1',nvme_config_space[int(self.l1ss_control1/4)].to_bytes(4,'big'))

    def get_l1ss(self, bus = 0, device = 0, function = 0):
        [a,b,c,d,self.l1ss_supported, self.aspm_L11_supported, self.aspm_L12_supported, self.pcipm_L11_supported, self.pcipm_L12_supported] = bitstruct.unpack('u8u8u8u3u1u1u1u1u1',nvme_config_space[int(self.l1ss_cap/4)].to_bytes(4,'big'))
        [a,b,c,d,self.aspm_L11_enable, self.aspm_L12_enable, self.pcipm_L11_enable, self.pcipm_L12_enable] = bitstruct.unpack('u8u8u8u4u1u1u1u1',nvme_config_space[int(self.l1ss_control1/4)].to_bytes(4,'big'))

    def get_cap_offset(self, bus = 0, device = 0, function = 0, offset = 0x34, cap_id_exp = 0):
        cap_id_found = 0
        addr = 0xC0000000 + ( bus << 20 ) + ( device << 15 ) + ( function<< 12 ) + offset
        offset_new = mem(addr,1)
        while((not cap_id_found) and (offset_new)):
            addr = 0xC0000000 + ( bus << 20 ) + ( device << 15 ) + ( function<< 12 ) + offset_new
            cap_id = mem(addr,1)
            if(cap_id != cap_id_exp):
                offset_new = mem(addr+1,1)
            else:
                cap_id_found = 1
        if(cap_id_found):
            return offset_new
        else:
            return 0
       
    def get_cap_offset1(self, cap_pointer = 0x34, cap_id_exp = 0):
        
        if(cap_pointer == 0x34):
            next_cap_pointer = nvme_config_space[int(cap_pointer/4)] & 0xFF
            while(next_cap_pointer != 0):
                cap_id = nvme_config_space[int(next_cap_pointer/4)] & 0xFF
                print(cap_id)
                if(cap_id == cap_id_exp):
                    break;
                else:
                    next_cap_pointer = nvme_config_space[int(next_cap_pointer/4)] & 0xFF00

        else:
            next_cap_pointer = cap_pointer
            while(next_cap_pointer != 0):
                cap_id           = nvme_config_space[int(next_cap_pointer/4)] & 0xFFFF
                if(cap_id == cap_id_exp):
                    break;
                else:
                    next_cap_pointer = ((nvme_config_space[int(next_cap_pointer/4)] & 0xFFF00000) >> 20)
        return next_cap_pointer

def main():
    pcie_container = pciecontainer()
    #print(hex(pcie_container.cfg_read(bus = 1, device = 0, function = 0)))
    #print(hex(pcie_container.cfg_read(bus = 0, device = 6, function = 0)))
    #print(hex(pcie_container.cfg_read(bus = 0, device = 10, function = 0)))
    #print(pcie_container.cfg_space_read(bus = 1, device = 0, function = 0))
    #pcie_container.cfg_space_load('c:\\bdf_1_0_0')
    pcie_container.scan_bus(256,32,8)

if __name__ == "__main__":
    main()
