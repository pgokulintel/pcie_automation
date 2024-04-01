import pickle
import bitstruct
from pcie_h import *
with open('nvme_100', 'rb') as f:
    nvme_config_space = pickle.load(f)


PCIE_EXT_CAP_PTR    =  0x100
PCIE_STD_CAP_PTR    =  0x34

PWR_STATE = {
    'D0'     : 0,
    'D1'     : 1,
    'D2'     : 2,
    'D3_HOT' : 3
    }

class pcie_utils(object):
    def __init__(self):
        print('pcie_utils')
        self.value = 0
        # PCI Common Registers
        self.vendor_id              = [ 0x00, 0x0 ]
        self.device_id              = [ 0x02, 0x0 ]
        self.command                = [ 0x04, 0x0 ]
        self.status                 = [ 0x06, 0x0 ]
        self.revision_id            = [ 0x08, 0x0 ]
        self.class_code             = [ 0x09, 0x0 ]
        self.header_type            = [ 0x0E, 0x0 ]
        
        self.primary_bus_number     = [ 0x18, 0x0 ]
        self.secondary_bus_number   = [ 0x19, 0x0 ]
        self.subordinate_bus_number = [ 0x1a, 0x0 ]
        
        self.l1ss_base              = self.get_offset(PCIE_EXT_CAP_PTR, pcie_ext_capabilities().PCI_EXT_CAP_ID_L1SS) # L1ss Id
        self.std_capability_base    = self.get_offset(PCIE_STD_CAP_PTR, pcie_std_capability_ids().PCI_CAP_ID_EXP) # EXP_CAP_ID
        
        self.l1ss_cap               = [ self.l1ss_reg_base + 0x04, 0 ]
        self.l1ss_control1          = [ self.l1ss_reg_base + 0x08, 0 ]
        self.l1ss_control2          = [ self.l1ss_reg_base + 0x0C, 0 ]    # For Future use
        self.l1ss_control1          = [ self.l1ss_reg_base + 0x10, 0 ]    # For Future use

        self.control = [self.exp_capability_base + 0x08, 0x0 ]
        self.status = [self.exp_capability_base + 0x0a, 0x0 ]
        self.capabilities = [self.exp_capability_base + 0x0c, 0x0 ]
        self.control = [self.exp_capability_base + 0x10, 0x0 ]
        self.status = [ 0x12, 0x0 ]
        self.capabilities = [ 0x14, 0x0 ]
        self.control = [ 0x18, 0x0 ]
        self.status = [ 0x1a, 0x0 ]
        self.control = [ 0x1c, 0x0 ]
        self.capabilities = [ 0x1e, 0x0 ]
        self.status = [ 0x20, 0x0 ]
        self.capabilities_2 = [ 0x24, 0x0 ]
        self.control_2 = [ 0x28, 0x0 ]
        self.status_2 = [ 0x2a, 0x0 ]
        self.capabilities_2 = [ 0x2c, 0x0 ]
        self.control_2 = [ 0x30, 0x0 ]
        self.status_2 = [ 0x32, 0x0 ]
        self.capabilities_2 = [ 0x34, 0x0 ]
        self.control_2 = [ 0x38, 0x0 ]
        self.status_2 = [ 0x3a, 0x0 ]
        self.capability_header_00, 0x0 ]
        self.control = [ 0xfor_msi_02, 0x0 ]
        self.get_l1ss()

        # PCI

    def pci_config_space(self):
        print(hex(nvme_config_space[0]))
        [self.vid, self.did]           = bitstruct.unpack('u16u16',nvme_config_space[0].to_bytes(4,'big'))
        [b,self.multi_fun,self.htype]  = bitstruct.unpack('u8u1u7',nvme_config_space[3].to_bytes(4,'big'))
        [self.bar0]                    = bitstruct.unpack('u32',nvme_config_space[4].to_bytes(4,'big'))
        [self.bar1]                    = bitstruct.unpack('u32',nvme_config_space[5].to_bytes(4,'big'))
        [self.bar2]                    = bitstruct.unpack('u32',nvme_config_space[6].to_bytes(4,'big'))
        [self.bar3]                    = bitstruct.unpack('u32',nvme_config_space[7].to_bytes(4,'big'))
        [self.bar4]                    = bitstruct.unpack('u32',nvme_config_space[8].to_bytes(4,'big'))
        [self.bar5]                    = bitstruct.unpack('u32',nvme_config_space[9].to_bytes(4,'big'))

       
    def set_d2hot(self, bus = 0, device = 0, function = 0):
        pwr_mgnt_control_reg_off = self.get_offset(PCIE_STD_CAP_PTR, pcie_std_capability_ids().PCI_CAP_ID_PM)
        add = 0xC0000000 + ( bus << 20 ) + ( device << 15 ) + ( function<< 12 ) + pwr_mgnt_control_reg_off
        val = mem(add+4,4) + PWR_STATE['D3HOT']        
        mem(add+4, 4, val)

    def read_cfg(self, bus, device, function, offset):
        add = 0xC0000000 + ( bus << 20 ) + ( device << 15 ) + ( function<< 12 ) + offset
        mem(add,4)

    def write_cfg(self, bus, device, function, offset, value):
        add = 0xC0000000 + ( bus << 20 ) + ( device << 15 ) + ( function<< 12 ) + offset
        mem(add, 4, value)

    def get_l1ss(self):
        [a,b,c,d,self.l1ss_supported, self.aspm_L11_supported, self.aspm_L12_supported, self.pcipm_L11_supported, self.pcipm_L12_supported] = bitstruct.unpack('u8u8u8u3u1u1u1u1u1',nvme_config_space[int(self.l1ss_cap/4)].to_bytes(4,'big'))
        [a,b,c,d,self.aspm_L11_enable, self.aspm_L12_enable, self.pcipm_L11_enable, self.pcipm_L12_enable] = bitstruct.unpack('u8u8u8u4u1u1u1u1',nvme_config_space[int(self.l1ss_control1/4)].to_bytes(4,'big'))

    def set_l1ss(self, bus, device, function):
            [a,b,c,d,self.l1ss_supported, self.aspm_L11_supported, self.aspm_L12_supported, self.pcipm_L11_supported, self.pcipm_L12_supported] = bitstruct.unpack('u8u8u8u3u1u1u1u1u1',nvme_config_space[int(self.l1ss_cap/4)].to_bytes(4,'big'))
            [a,b,c,d,self.aspm_L11_enable, self.aspm_L12_enable, self.pcipm_L11_enable, self.pcipm_L12_enable] = bitstruct.unpack('u8u8u8u4u1u1u1u1',nvme_config_space[int(self.l1ss_control1/4)].to_bytes(4,'big'))

    def get_expr_capability(self):
        

    def get_offset(self, cap_pointer = 0x34, cap_id_exp = 0):
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
    s = pcie_utils()
    s.pcie_decoder()

if __name__ == "__main__":
    main()
