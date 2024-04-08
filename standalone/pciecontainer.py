from prettytable import PrettyTable
from enum import Enum
import pickle
from arrowlake.pcie_utils.pcie_h import *
import bitstruct
import ipccli as _ipccli
itp = _ipccli.baseaccess()

PCIE_STD_CAP_PTR= 0x34

class pcie_cap(object):
    def __init__(self):
        self.pcie_id             = pcie_cap_ids().pciexp
        self.pcieext_id_l1ss     = pcie_ext_cap_ids().l1ss
        self.pcieext_id_ltr      = pcie_ext_cap_ids().l1ss
        self.did                 = 0
        self.bdf                 = []
        self.sec_bus             = 0
        self.bar0                = 0
        self.device_state        = 0
        self.max_linkspeed       = 0
        self.max_linkwidth       = 0
        self.mps_support         = 0
        self.L0s_support         = 0
        self.L1_support          = 0
        self.aspm_L1_1_support   = 0
        self.aspm_L1_2_support   = 0
        self.pcipm_L1_1_support  = 0
        self.pcipm_L1_2_support  = 0

        self.etag_support        = 0
        
        self.nego_linkspeed      = 0
        self.nego_linkwidth      = 0
        self.nego_mps            = 0
        self.L0s_enable          = 0
        self.L1_enable           = 0
        self.aspm_L1_1_enable    = 0
        self.aspm_L1_2_enable    = 0
        self.pcipm_L1_1_enable   = 0
        self.pcipm_L1_2_enable   = 0

class pciecontainer():
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

        didvid = self.cfg_read(bus, device, function, offset = 0)
        vid = didvid & 0xFFFF
        if(vid in did_vid):
            return [didvid,did_vid[vid]]
        else:
            return [didvid,hex(didvid)]

    def get_ddid(self, bus = 0, device = 0, function = 0):

        sbus = self.get_secbus_num(bus, device, function)
        didvid = self.get_did(bus = sbus)
        vid = didvid[0] & 0xFFFF
        print(hex(vid))
        if(sbus == 0):
            return [0, 'None']
        else:
            if(didvid[0] == 0xFFFFFFFF):
                return [0, 'None']
            else:
                if(vid in did_vid):
                    return [hex(didvid[0]),did_vid[vid]]
                else:
                    return [hex(didvid[0]),hex(didvid[0])]
        
        
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
                        did = self.get_did(bus, device, function)
                        ddid = self.get_ddid(bus, device, function)
                        if(ddid[0] == 0):
                            ddid = 'None'
                        else:
                            ddid = '{0} ({1})'.format(ddid[0],ddid[1])
                        pcie_ports.add_row([ port, bus, device, function,
                                             hex(did[0]),
                                             hex(self.get_secbus_num(bus, device, function)),
                                             ddid])
                        #print('Bus {0}, device {1}, function {2}, did {3}'.format(bus,device,function,hex(did)))
        print(pcie_ports)

    def get_device_state(self, bus = 0, device = 0, function = 0):
        return 0

    def get_lpm_supported(self, bus = 0, device = 0, function = 0):
        return 0

    def get_lpm_enabled(self, bus = 0, device = 0, function = 0):
        return 0
    def get_mps_support(self, bus = 0, device = 0, function = 0):
        return 0

    def get_l1ss_offset(self, bus = 0, device = 0, function = 0):
        pcie_ext_offset = self.get_cap_offset(bus, device, function, offset = 0x100, cap_id_exp = pcie_ext_cap_ids().l1ss )
        pcie_l1ssctl1 = pcie_ext_offset + pcie_ext_aspm().l1ss_ctl1
        return pcie_l1ssctl1
    
    def get_aspm_offset(self, bus = 0, device = 0, function = 0):
        pcie_offset = self.get_cap_offset(bus, device, function)
        return pcie_offset + 0x10
        
    def set_l1ss(self, bus = 0, device = 0, function = 0, aspm_L1_1 = 1, aspm_L1_2 = 1, pcipm_L1_1 = 1, pcipm_L1_2 = 1):
        l1ss_offset = self.get_l1ss_offset(bus,device,function)
        read_val = self.cfg_read(bus,device,function, offset=l1ss_offset,size=1)
        addr = self.get_pcie_mmio_addr(bus, device,function,l1ss_offset)
        write_val = (read_val & 0xFFFFFFF0) | pcipm_L1_2 | (pcipm_L1_1 << 1) | (aspm_L1_2<<2) | (aspm_L1_1<<3)
        mem(addr, 1, write_val)
        
    def set_aspm(self, bus = 0, device = 0, function = 0, aspm_L0s = 1, aspm_L1 = 1):
        aspm_offset = self.get_aspm_offset(bus,device,function)
        read_val = self.cfg_read(bus,device,function, offset=aspm_offset,size=1)
        addr = self.get_pcie_mmio_addr(bus, device,function,aspm_offset)
        write_val = (read_val & 0xFFFFFFFC) | aspm_L0s | (aspm_L1 << 1)
        mem(addr, 1, write_val)

   
    def get_cap(self, bus = 0, device = 0, function = 0):
        pciecap = pcie_cap()
        pcie_offset = self.get_cap_offset(bus,device,function)
        pcie_ext_offset = self.get_cap_offset(bus, device, function, offset = 0x100, cap_id_exp = pcie_ext_cap_ids().l1ss )

        #device capabilities
        pcie_devcap = pcie_offset + pcie_cap_registers().devcap
        val = self.cfg_read(bus, device, function, offset = pcie_devcap, size = 1)
        [x, pciecap.etag_support, x, pciecap.mps_support] = bitstruct.unpack('u2u1u2u3',val.to_bytes(1,'big'))

        #device control
        pcie_devcntl = pcie_offset + pcie_cap_registers().devctl
        val = self.cfg_read(bus, device, function, offset = pcie_devcntl, size = 2)
        [x, pciecap.max_read_request_size, pciecap.no_snoop, pciecap.aux_power, phatom, pciecap.etag_en, pciecap.nego_mps, pciecap.ro, x,x,x,x]= bitstruct.unpack('u1u3u1u1u1u1u3u1u1u1u1u1',val.to_bytes(2,'big'))

        #Link Cap
        pcie_linkcap = pcie_offset + pcie_cap_registers().lnkcap
        val = self.cfg_read(bus, device, function, offset = pcie_linkcap, size = 2)
        [x, pciecap.L1_support, pciecap.L0s_support, pciecap.max_linkwidth, pciecap.max_linkspeed]= bitstruct.unpack('u4u1u1u6u4',val.to_bytes(2,'big'))

        #Link control
        pcie_linkcntl = pcie_offset + pcie_cap_registers().lnkctl
        val = self.cfg_read(bus, device, function, offset = pcie_linkcntl, size = 1)
        [x,pciecap.L1_enable, pciecap.L0s_enable]= bitstruct.unpack('u6u1u1',val.to_bytes(1,'big'))
        
        #Link status
        pcie_linksts = pcie_offset + pcie_cap_registers().lnksta
        val = self.cfg_read(bus, device, function, offset = pcie_linksts, size = 2)
        [x,pciecap.nego_linkwidth, pciecap.nego_linkspeed]= bitstruct.unpack('u6u6u4',val.to_bytes(2,'big'))
        pciecap.did  = hex(self.get_did(bus,device,function)[0])
        pciecap.bdf  =[bus,device,function]
        pciecap.sbus = self.get_secbus_num(bus,device,function)
        pciecap.bar0 = self.cfg_read(bus,device,function,0x10)
        pciecap.bar1 = self.cfg_read(bus,device,function,0x14)

        #L1ss capabilities
        pcie_l1sscap = pcie_ext_offset + pcie_ext_aspm().l1ss_cap
        print(pcie_l1sscap)
        val = self.cfg_read(bus, device, function, offset = pcie_l1sscap, size = 1)
        [x, pciecap.L1_pm_ss_supported, pciecap.aspm_L1_1_support, pciecap.aspm_L1_2_support, pciecap.pcipm_L1_1_support, pciecap.pcipm_L1_2_support] = bitstruct.unpack('u3u1u1u1u1u1',val.to_bytes(1,'big'))

        #L1ss control
        pcie_l1ssctl1 = pcie_ext_offset + pcie_ext_aspm().l1ss_ctl1
        val = self.cfg_read(bus, device, function, offset = pcie_l1ssctl1, size = 1)
        [x, pciecap.aspm_L1_1_enable, pciecap.aspm_L1_2_enable, pciecap.pcipm_L1_1_enable, pciecap.pcipm_L1_2_enable] = bitstruct.unpack('u4u1u1u1u1',val.to_bytes(1,'big'))
       
        return pciecap
        

    def print_attribute(self,obj = None):
        for i in (vars(obj)):
            print("{0:10}: {1}".format(i, vars(obj)[i]))
        #print(vars(pciecap))

    def print_capabilities(self, bus = 0, device = 0, function = 0):
        field_names          = ['parameter' , 'Root Port', 'EndPoint']
        pci_cap1             = self.get_cap(bus,device,function)
        sec_bus = self.get_secbus_num(bus,device,function)
        pci_cap2             = self.get_cap(sec_bus)
        cfg_cap              = PrettyTable()
        cfg_cap.title        = "Root Port and End Point Capabilitiy and Negotiated"
        cfg_cap.field_names  = field_names
        cfg_cap.add_row([ "Device ID",pci_cap1.did, pci_cap2.did])
        cfg_cap.add_row([ "BDF",pci_cap1.bdf, pci_cap2.bdf])        
        cfg_cap.add_row([ "Device State",pwr_state[pci_cap1.device_state], pwr_state[pci_cap2.device_state]])
#        cfg_cap.add_row([ "Link State",'-', '-'])
        cfg_cap.add_row([ "Max Speed",linkspeed[pci_cap1.max_linkspeed],linkspeed[pci_cap2.max_linkspeed]])
        cfg_cap.add_row([ "Max Width",pci_cap1.max_linkwidth, pci_cap2.max_linkwidth])
        cfg_cap.add_row([ "Max Payload",payload[pci_cap1.mps_support], payload[pci_cap2.mps_support]])
        cfg_cap.add_row([ "Sec Bus",pci_cap1.sbus, pci_cap2.sbus])
        cfg_cap.add_row([ "Bar0",hex(pci_cap1.bar0), hex(pci_cap2.bar0)])
        cfg_cap.add_row([ "Bar1",hex(pci_cap1.bar1), hex(pci_cap2.bar1)])
        cfg_cap.add_row([ "ASPM L0s Support",pci_cap1.L0s_support, pci_cap2.L0s_support])
        cfg_cap.add_row([ "ASPM L1 Support",pci_cap1.L1_support, pci_cap2.L1_support])
        cfg_cap.add_row([ "ASPM L1.1 Support",pci_cap1.aspm_L1_1_support, pci_cap2.aspm_L1_1_support])
        cfg_cap.add_row([ "ASPM L1.2 Support",pci_cap1.aspm_L1_1_support, pci_cap2.aspm_L1_1_support])
        cfg_cap.add_row([ "PCIPM L1.1 Support",pci_cap1.pcipm_L1_1_support, pci_cap2.pcipm_L1_1_support])
        cfg_cap.add_row([ "PCIPM L1.2 Support",pci_cap1.pcipm_L1_2_support, pci_cap2.pcipm_L1_2_support])

        cfg_cap.add_row([ "Payload Negotiated",payload[pci_cap1.nego_mps], payload[pci_cap2.nego_mps]])
        cfg_cap.add_row([ "ASPM L0s Enable",pci_cap1.L0s_enable, pci_cap2.L0s_enable])
        cfg_cap.add_row([ "ASPM L1 Enable",pci_cap1.L1_enable, pci_cap2.L1_enable])
 #       cfg_cap.add_row([ "PCIPM L1 (D3Hot) Enable",'-', '-'])
        cfg_cap.add_row([ "ASPM L1.1 Enable",pci_cap1.aspm_L1_1_enable, pci_cap2.aspm_L1_1_enable])
        cfg_cap.add_row([ "ASPM L1.2 Enable",pci_cap1.aspm_L1_2_enable, pci_cap2.aspm_L1_2_enable])
        cfg_cap.add_row([ "PCIPM L1.1 Enable",pci_cap1.pcipm_L1_1_enable, pci_cap2.pcipm_L1_1_enable])
        cfg_cap.add_row([ "PCIPM L1.2 Enable",pci_cap1.pcipm_L1_2_enable, pci_cap2.pcipm_L1_2_enable])
        print(cfg_cap)


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

    def set_l1ss1(self, bus, device, function):
            [a,b,c,d,self.l1ss_supported, self.aspm_L11_supported, self.aspm_L12_supported, self.pcipm_L11_supported, self.pcipm_L12_supported] = bitstruct.unpack('u8u8u8u3u1u1u1u1u1',nvme_config_space[int(self.l1ss_cap/4)].to_bytes(4,'big'))
            [a,b,c,d,self.aspm_L11_enable, self.aspm_L12_enable, self.pcipm_L11_enable, self.pcipm_L12_enable] = bitstruct.unpack('u8u8u8u4u1u1u1u1',nvme_config_space[int(self.l1ss_control1/4)].to_bytes(4,'big'))

    def get_l1ss(self, bus = 0, device = 0, function = 0):
        [a,b,c,d,self.l1ss_supported, self.aspm_L11_supported, self.aspm_L12_supported, self.pcipm_L11_supported, self.pcipm_L12_supported] = bitstruct.unpack('u8u8u8u3u1u1u1u1u1',nvme_config_space[int(self.l1ss_cap/4)].to_bytes(4,'big'))
        [a,b,c,d,self.aspm_L11_enable, self.aspm_L12_enable, self.pcipm_L11_enable, self.pcipm_L12_enable] = bitstruct.unpack('u8u8u8u4u1u1u1u1',nvme_config_space[int(self.l1ss_control1/4)].to_bytes(4,'big'))

    def get_cap_offset(self, bus = 0, device = 0, function = 0, offset = 0x34, cap_id_exp = 0x10):
        cap_id_found = 0
        if(offset == 0x34):
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
        else:
            addr = 0xC0000000 + ( bus << 20 ) + ( device << 15 ) + ( function<< 12 ) + offset
            offset_new = offset
            while((not cap_id_found) and (offset_new)):
                addr = 0xC0000000 + ( bus << 20 ) + ( device << 15 ) + ( function<< 12 ) + offset_new
                cap_id = mem(addr,4) &0xFFFF
                if(cap_id != cap_id_exp):
                    offset_new =  mem(addr,4) >> 20
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
    #pcie_container.scan_bus(3,15,3)
    #pcie_container.print_capabilities(0,6,0)
    #print(hex(pcie_container.get_did(1,0,0)))
    pcie_container.set_aspm(1,0,0,1,1)
   # pcie_container.set_aspm(1,0,0,1,1)
    #pcie_container.set_l1ss(0,6,0,0,0,0,0)
    #pcie_container.set_l1ss(0,6,0,1,1,1,1)

if __name__ == "__main__":
    main()
