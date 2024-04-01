class did_vid(object):
    def __init__(self):
        self.did = {
                    0x144D : 'SAMSUNG',
                    0x15b7 : 'WD'
                    }

PWR_STATE = {
    'D0'     : 0,
    'D1'     : 1,
    'D2'     : 2,
    'D3_HOT' : 3
    }

class config_space(object):
    def __init__(self):        
        # PCI Configuration Space 256
        # PCI Express Configuration Space 4096
        self.cfg_space_size     = 256
        self.cfg_space_exp_size = 4096
        self.std_header_sizeof = 64
        self.std_num_bars      = 6           # number of standard bars 
        
        self.vendor_id         = 0x00        # 16 bits 
        self.device_id         = 0x02        # 16 bits 
        self.command           = 0x04        # 16 bits 
        self.status            = 0x06        # 16 bits 
        self.class_revision    = 0x08        # high 24 bits are class, low 8 revision 
        self.revision_id       = 0x08        # revision id 
        self.class_prog        = 0x09        # reg. level programming interface 
        self.class_device      = 0x0a        # device class 
        self.cache_line_size   = 0x0c        # 8 bits 
        self.latency_timer     = 0x0d        # 8 bits 
        self.header_type       = 0x0e        # 8 bits 
        self.header_type_mask  = 0x7f
        self.header_type_normal  = 0
        self.header_type_bridge  = 1
        self.header_type_cardbus = 2
        self.header_type_mfd     = 0x80          # m ti-function device (possible) 
        self.bist                = 0x0f            # 8 bits 
        self.bist_code_mask      = 0x0f            # return res t 
        self.bist_start          = 0x40            # 1 to start bist, 2 secs or less 
        self.bist_capable        = 0x80            # 1 if bist capable 
        self.base_address_0      = 0x10            # 32 bits 
        self.base_address_1      = 0x14            # 32 bits [htype 0,1 only] 
        self.base_address_2      = 0x18            # 32 bits [htype 0 only] 
        self.base_address_3      = 0x1c            # 32 bits 
        self.base_address_4      = 0x20            # 32 bits 
        self.base_address_5      = 0x24            # 32 bits 
        self.base_address_space         = 0x01     # 0 = memory, 1 = i/o 
        self.base_address_space_io      = 0x01
        self.base_address_space_memory  = 0x00
        self.base_address_mem_type_mask = 0x06
        self.base_address_mem_type_32   = 0x00     # 32 bit address 
        self.base_address_mem_type_1m   = 0x02     # below 1m [obsolete] 
        self.base_address_mem_type_64   = 0x04     # 64 bit address 
        self.base_address_mem_prefetch  = 0x08     # prefetchable? 
        self.base_address_mem_mask      = (~0x0f )
        self.base_address_io_mask       = (~0x03 )

        # header type 0 (normal devices) 
        self.cardbus_cis                = 0x28
        self.subsystem_vendor_id        = 0x2c
        self.subsystem_id               = 0x2e
        self.rom_address                = 0x30      # bits 31..11 are address, 10..1 reserved 
        self.rom_address_enable         = 0x01
        self.rom_address_mask           = (~0x7ff )

        self.capability_list            = 0x34      # offset of first capability list entry 

        # 0x35-0x3b are reserved 
        self.interrupt_line             = 0x3c      # 8 bits 
        self.interrupt_pin              = 0x3d      # 8 bits 
        self.min_gnt                    = 0x3e      # 8 bits 
        self.max_lat                    = 0x3f      # 8 bits 

        # header type 1 (pci-to-pci bridges) 
        self.primary_bus                = 0x18      # primary bus number 
        self.secondary_bus              = 0x19      # secondary bus number 
        self.subordinate_bus            = 0x1a            # highest bus number behind the bridge 
        self.sec_latency_timer          = 0x1b            # latency timer for secondary interface 
        self.io_base = 0x1c            # i/o range behind the bridge 
        self.io_limit = 0x1d
        self.io_range_type_mask = 0x0f             # i/o bridging type 
        self.io_range_type_16 = 0x00
        self.io_range_type_32 = 0x01
        self.io_range_mask = (~0x0f ) # standard 4k i/o windows 
        self.io_1k_range_mask = (~0x03 ) # intel 1k i/o windows 
        self.sec_status = 0x1e            # secondary status register, only bit 14 used 
        self.memory_base = 0x20            # memory range behind 
        self.memory_limit = 0x22
        self.memory_range_type_mask = 0x0f 
        self.memory_range_mask = (~0x0f )
        self.pref_memory_base = 0x24            # prefetchable memory range behind 
        self.pref_memory_limit = 0x26
        self.pref_range_type_mask = 0x0f 
        self.pref_range_type_32 = 0x00
        self.pref_range_type_64 = 0x01
        self.pref_range_mask = (~0x0f )
        self.pref_base_upper32 = 0x28            # upper half of prefetchable memory range 
        self.pref_limit_upper32 = 0x2c
        self.io_base_upper16 = 0x30            # upper half of i/o addresses 
        self.io_limit_upper16 = 0x32
        # 0x34 same as for htype 0 
        # 0x35-0x3b is reserved 
        self.rom_address1 = 0x38            # same as rom_address, but for htype 1 
        # 0x3c-0x3d are same as for htype 0 
        self.bridge_control = 0x3e
        self.bridge_ctl_parity = 0x01            # enable parity detection on secondary interface 
        self.bridge_ctl_serr = 0x02            # the same for serr forwarding 
        self.bridge_ctl_isa = 0x04            # enable isa mode 
        self.bridge_ctl_vga = 0x08            # forward vga addresses 
        self.bridge_ctl_master_abort = 0x20  # report master aborts 
        self.bridge_ctl_bus_reset = 0x40            # secondary bus reset 
        self.bridge_ctl_fast_back = 0x80            # fast back2back enabled on secondary interface 

        # header type 2 (cardbus bridges) 
        self.cb_capability_list = 0x14
        # 0x15 reserved 
        self.cb_sec_status = 0x16            # secondary status 
        self.cb_primary_bus = 0x18            # pci bus number 
        self.cb_card_bus = 0x19            # cardbus bus number 
        self.cb_subordinate_bus = 0x1a            # subordinate bus number 
        self.cb_latency_timer = 0x1b            # cardbus latency timer 
        self.cb_memory_base_0 = 0x1c
        self.cb_memory_limit_0 = 0x20
        self.cb_memory_base_1 = 0x24
        self.cb_memory_limit_1 = 0x28
        self.cb_io_base_0 = 0x2c
        self.cb_io_base_0_hi = 0x2e
        self.cb_io_limit_0 = 0x30
        self.cb_io_limit_0_hi = 0x32
        self.cb_io_base_1 = 0x34
        self.cb_io_base_1_hi = 0x36
        self.cb_io_limit_1 = 0x38
        self.cb_io_limit_1_hi = 0x3a
        self.cb_io_range_mask = (~0x03 )
        # 0x3c-0x3d are same as for htype 0 
        self.cb_bridge_control = 0x3e
        self.cb_bridge_ctl_parity = 0x01            # similar to standard bridge control register 
        self.cb_bridge_ctl_serr = 0x02
        self.cb_bridge_ctl_isa = 0x04
        self.cb_bridge_ctl_vga = 0x08
        self.cb_bridge_ctl_master_abort = 0x20
        self.cb_bridge_ctl_cb_reset = 0x40            # cardbus reset 
        self.cb_bridge_ctl_16bit_int = 0x80            # enable interrupt for 16-bit cards 
        self.cb_bridge_ctl_prefetch_mem0 = 0x100            # prefetch enable for both memory regions 
        self.cb_bridge_ctl_prefetch_mem1 = 0x200
        self.cb_bridge_ctl_post_writes = 0x400
        self.cb_subsystem_vendor_id = 0x40
        self.cb_subsystem_id = 0x42
        self.cb_legacy_mode_base = 0x44            # 16-bit pc card legacy mode base address (exca) 
        # 0x48-0x7f reserved 
    
class pcie_cap_ids(object):
    def __init__(self):
        # capability lists 
        self.base_add      = 0x34    # Traverse to all Cap ID
        self.cap_list_id   = 0x0     # capability id 
        self.pm            = 0x1     # power management
        self.agp           = 0x2     # accelerated graphics port 
        self.vpd    = 0x3            # vital product data 
        self.slotid = 0x4            # slot identification 
        self.msi    = 0x5            # message signalled interrupts 
        self.chswp  = 0x6            # compactpci hotswap 
        self.pcix   = 0x7            # pci-x 
        self.ht     = 0x8            # hypertransport 
        self.vndr   = 0x9            # vendor-specific 
        self.dbg    = 0xa            # debug port 
        self.ccrc   = 0xb            # compactpci central resource control 
        self.shpc   = 0xc            # pci standard hot-plug controller 
        self.ssvid  = 0xd            # bridge subsystem vendor/device id 
        self.agp3   = 0xe            # agp target pci-pci bridge 
        self.secdev = 0xf            # secure device 
        self.pciexp    = 0x10           # pci express 
        self.msix   = 0x11           # msi-x 
        self.sata   = 0x12           # sata data/index conf. 
        self.af     = 0x13           # pci advanced features 
        self.ea     = 0x14           # pci enhanced allocation 
        self.max    = 0x15      

class pcie_ext_cap_ids(object):
    def __init__(self):
        # extended capabilities (pci-x 2.0 and express) 
        #self.ext_cap_id(header) = (header & 0x0000ffff)
        #self.ext_cap_ver(header) = ((header >> 16) & 0xf)
        #self.ext_cap_next(header) = ((header >> 20) & 0xffc)
        self.base_add = 0x100
        self.err = 0x01            # advanced error reporting 
        self.vc  = 0x02            # virtual channel capability 
        self.dsn = 0x03            # device serial number 
        self.pwr = 0x04            # power budgeting 
        self.rcld = 0x05            # root complex link declaration 
        self.rcilc = 0x06            # root complex internal link control 
        self.rcec = 0x07            # root complex event collector 
        self.mfvc = 0x08            # m ti-function vc capability 
        self.vc9 = 0x09            # same as _vc 
        self.rcrb = 0x0a            # root complex rb? 
        self.vndr = 0x0b            # vendor-specific 
        self.cac = 0x0c            # config access - obsolete 
        self.acs = 0x0d            # access control services 
        self.ari = 0x0e            # alternate routing id 
        self.ats = 0x0f            # address translation services 
        self.sriov = 0x10            # single root i/o virtualization 
        self.mriov = 0x11            # m ti root i/o virtualization 
        self.mcast = 0x12            # m ticast 
        self.pri = 0x13            # page request interface 
        self.amd_xxx = 0x14            # reserved for amd 
        self.rebar = 0x15            # resizable bar 
        self.dpa = 0x16            # dynamic power allocation 
        self.tph = 0x17            # tph requester 
        self.ltr = 0x18            # latency tolerance reporting 
        self.secpci = 0x19            # secondary pcie capability 
        self.pmux = 0x1a            # protocol m tiplexing 
        self.pasid = 0x1b            # process address space id 
        self.dpc = 0x1d            # downstream port containment 
        self.l1ss = 0x1e            # l1 pm substates 
        self.ptm = 0x1f            # precision time measurement 
        self.dvsec = 0x23            # designated vendor-specific 
        self.dlf = 0x25            # data link feature 
        self.pl_16gt = 0x26            # physical layer 16.0 gt/s 
        self.pl_32gt = 0x2a    # physical layer 32.0 gt/s 
        self.doe = 0x2e            # data object exchange 
        self.max = sellf.doe

        self.ext_cap_dsn_sizeof = 12
        self.ext_cap_mcast_endpoint_sizeof = 40

class pcie_capabilities(object):
    def __init__(self):
        self.ids            = pcie_cap_ids()
        self.regs           = [ pcie_pm_registers(),
                                pcie_msi_registers(),
                                pcie_cap_registers()]
        self.ext_ids        = pcie_ext_cap_ids()
        self.ext_regs       = [ pcie_ext_aer(),
                                pcie_ext_aspm(),
                                pcie_ext_ptm()]
    
class pcie_pm_registers(object):
    def __init__(self):
        
        # power management registers
        self.id = 0x1
        self.std_cap = 1
        self.pm_pmc_base =  0                     # get live data
        self.pm_pmc = 2                           # pm capabilities register 
        self.pm_cap_ver_mask = 0x0007             # version 
        self.pm_cap_pme_clock = 0x0008            # pme clock required 
        self.pm_cap_reserved = 0x0010             # reserved field 
        self.pm_cap_dsi = 0x0020                  # device specific initialization 
        self.pm_cap_aux_power = 0x01c0            # auxiliary power support mask 
        self.pm_cap_d1 = 0x0200                   # d1 power state support 
        self.pm_cap_d2 = 0x0400                   # d2 power state support 
        self.pm_cap_pme = 0x0800                  # pme pin supported 
        self.pm_cap_pme_mask = 0xf800             # pme mask of all supported states 
        self.pm_cap_pme_d0 = 0x0800               # pme#  from d0 
        self.pm_cap_pme_d1 = 0x1000               # pme#  from d1 
        self.pm_cap_pme_d2 = 0x2000               # pme#  from d2 
        self.pm_cap_pme_d3hot = 0x4000            # pme#  from d3 (hot) 
        self.pm_cap_pme_d3cold = 0x8000           # pme#  from d3 (cold) 
        self.pm_cap_pme_shift = 11                # start of the pme mask in pmc 
        self.pm_ctrl = 4                          # pm control and status register 
        self.pm_ctrl_state_mask = 0x0003          # current power state (d0 to d3) 
        self.pm_ctrl_no_soft_reset = 0x0008       # no reset for d3hot->d0 
        self.pm_ctrl_pme_enable = 0x0100          # pme pin enable 
        self.pm_ctrl_data_sel_mask = 0x1e00       # data select (??) 
        self.pm_ctrl_data_scale_mask = 0x6000     # data scale (??) 
        self.pm_ctrl_pme_status = 0x8000          # pme pin status 
        self.pm_ppb_extensions = 6                # ppb support extensions (??) 
        self.pm_ppb_b2_b3 = 0x40                  # stop clock when in d3hot (??) 
        self.pm_bpcc_enable = 0x80                # bus power/clock control enable (??) 
        self.pm_data_register = 7                 # (??) 
        self.pm_sizeof = 8

class pcie_msi_registers(object):
    def __init__(self):
        
        # message signaled interrupt registers 
        self.id = 0x5
        self.std_cap = 1
        self.msi_flags = 0x02            # message control 
        self.msi_flags_enable = 0x0001            # msi feature enabled 
        self.msi_flags_qmask = 0x000e            # maximum queue size available 
        self.msi_flags_qsize = 0x0070            # message queue size configured 
        self.msi_flags_64bit = 0x0080            # 64-bit addresses allowed 
        self.msi_flags_maskbit = 0x0100            # per-vector masking capable 
        self.msi_rfu = 3            # rest of capability flags 
        self.msi_address_lo = 0x04            # lower 32 bits 
        self.msi_address_hi = 0x08            # upper 32 bits (if msi_flags_64bit set) 
        self.msi_data_32 = 0x08            # 16 bits of data for 32-bit devices 
        self.msi_mask_32 = 0x0c            # mask bits register for 32-bit devices 
        self.msi_pending_32 = 0x10            # pending intrs for 32-bit devices 
        self.msi_data_64 = 0x0c            # 16 bits of data for 64-bit devices 
        self.msi_mask_64 = 0x10            # mask bits register for 64-bit devices 
        self.msi_pending_64 = 0x14            # pending intrs for 64-bit devices 

        # msi-x registers (in msi-x capability) 
        self.msix_flags = 2            # message control 
        self.msix_flags_qsize = 0x07ff            # table size 
        self.msix_flags_maskall = 0x4000            # mask all vectors for this function 
        self.msix_flags_enable = 0x8000            # msi-x enable 
        self.msix_table = 4            # table offset 
        self.msix_table_bir = 0x00000007 # bar index 
        self.msix_table_offset = 0xfffffff8 # offset into specified bar 
        self.msix_pba = 8            # pending bit array offset 
        self.msix_pba_bir = 0x00000007 # bar index 
        self.msix_pba_offset = 0xfffffff8 # offset into specified bar 
        self.msix_flags_birmask = msix_pba_bir # deprecated 
        self.cap_msix_sizeof = 12            # size of msix registers 

        # msi-x table entry format (in memory mapped by a bar) 
        self.msix_entry_size = 16
        self.msix_entry_lower_addr = 0x0  # message address 
        self.msix_entry_upper_addr = 0x4  # message upper address 
        self.msix_entry_data = 0x8  # message data 
        self.msix_entry_vector_ctrl = 0xc  # vector control 
        self.msix_entry_ctrl_maskbit = 0x00000001

class pcie_cap_struct_registers(object):
    def __init__(self):
        
        # pci express capability registers 
        self.id                            = 0x10
        self.offset                        = 0x0
        self.std_cap = 1
        self.pcie_cap                     = 0x02           # capabilities register 
        self.pcie_cap_vers            = 0x000f         # capability version 
        self.pcie_cap_type            = 0x00f0         # device/port type 
        self.pcie_cap_type_endpoint         = 0x0            # express endpoint 
        self.pcie_cap_type_leg_end          = 0x1            # legacy endpoint 
        self.pcie_cap_type_root_port        = 0x4            # root port 
        self.pcie_cap_type_upstream         = 0x5            # upstream port 
        self.pcie_cap_type_downstream       = 0x6            # downstream port 
        self.pcie_cap_type_pci_bridge       = 0x7            # pcie to pci/pci-x bridge 
        self.pcie_cap_type_pcie_bridge      = 0x8            # pci/pci-x to pcie bridge 
        self.pcie_cap_type_rc_end           = 0x9            # root complex integrated endpoint 
        self.pcie_cap_type_rc_ec            = 0xa            # root complex event collector 
        self.pcie_cap_slot                  = 0x0100         # slot implemented 
        self.pcie_cap_flags_irq             = 0x3e00         # interrupt message number 
        self.devcap                = 0x04           # device capabilities 
        self.devcap_payload        = 0x00000007 # max_payload_size 
        self.devcap_phantom = 0x00000018 # phantom functions 
        self.devcap_ext_tag = 0x00000020 # extended tags 
        self.devcap_l0s = 0x000001c0 # l0s acceptable latency 
        self.devcap_l1 = 0x00000e00 # l1 acceptable latency 
        self.devcap_atn_but = 0x00001000 # attention button present 
        self.devcap_atn_ind = 0x00002000 # attention indicator present 
        self.devcap_pwr_ind = 0x00004000 # power indicator present 
        self.devcap_rber = 0x00008000 # role-based error reporting 
        self.devcap_pwr_val = 0x03fc0000 # slot power limit value 
        self.devcap_pwr_scl = 0x0c000000 # slot power limit scale 
        self.devcap_flr = 0x10000000 # function level reset 
        self.devctl = 0x08            # device control 
        self.devctl_cere = 0x0001            # correctable error reporting en. 
        self.devctl_nfere = 0x0002            # non-fatal error reporting enable 
        self.devctl_fere = 0x0004            # fatal error reporting enable 
        self.devctl_urre = 0x0008            # unsupported request reporting en. 
        self.devctl_relax_en=0x0010 # enable relaxed ordering 
        self.devctl_payload = 0x00e0            # max_payload_size 
        self.devctl_payload_128b = 0x0000 # 128 bytes 
        self.devctl_payload_256b = 0x0020 # 256 bytes 
        self.devctl_payload_512b = 0x0040 # 512 bytes 
        self.devctl_payload_1024b = 0x0060 # 1024 bytes 
        self.devctl_payload_2048b = 0x0080 # 2048 bytes 
        self.devctl_payload_4096b = 0x00a0 # 4096 bytes 
        self.devctl_ext_tag = 0x0100            # extended tag field enable 
        self.devctl_phantom = 0x0200            # phantom functions enable 
        self.devctl_aux_pme = 0x0400            # auxiliary power pm enable 
        self.devctl_nosnoop_en = 0x0800  # enable no snoop 
        self.devctl_readrq = 0x7000            # max_read_request_size 
        self.devctl_readrq_128b =  0x0000 # 128 bytes 
        self.devctl_readrq_256b =  0x1000 # 256 bytes 
        self.devctl_readrq_512b = 0x2000 # 512 bytes 
        self.devctl_readrq_1024b = 0x3000 # 1024 bytes 
        self.devctl_readrq_2048b = 0x4000 # 2048 bytes 
        self.devctl_readrq_4096b = 0x5000 # 4096 bytes 
        self.devctl_bcr_flr = 0x8000  # bridge configuration retry / flr 
        self.devsta = 0x0a            # device status 
        self.devsta_ced = 0x0001            # correctable error detected 
        self.devsta_nfed = 0x0002            # non-fatal error detected 
        self.devsta_fed = 0x0004            # fatal error detected 
        self.devsta_urd = 0x0008            # unsupported request detected 
        self.devsta_auxpd = 0x0010            # aux power detected 
        self.devsta_trpnd = 0x0020            # transactions pending 
        self.cap_exp_rc_endpoint_sizeof_v1 = 12            # v1 endpoints without link end here 
        self.lnkcap = 0x0c            # link capabilities 
        self.lnkcap_sls = 0x0000000f # supported link speeds 
        self.lnkcap_sls_2_5gb = 0x00000001 # lnkcap2 sls vector bit 0 
        self.lnkcap_sls_5_0gb = 0x00000002 # lnkcap2 sls vector bit 1 
        self.lnkcap_sls_8_0gb = 0x00000003 # lnkcap2 sls vector bit 2 
        self.lnkcap_sls_16_0gb = 0x00000004 # lnkcap2 sls vector bit 3 
        self.lnkcap_sls_32_0gb = 0x00000005 # lnkcap2 sls vector bit 4 
        self.lnkcap_sls_64_0gb = 0x00000006 # lnkcap2 sls vector bit 5 
        self.lnkcap_mlw = 0x000003f0 # maximum link width 
        self.lnkcap_aspms = 0x00000c00 # aspm support 
        self.lnkcap_aspm_l0s = 0x00000400 # aspm l0s support 
        self.lnkcap_aspm_l1 = 0x00000800 # aspm l1 support 
        self.lnkcap_l0sel = 0x00007000 # l0s exit latency 
        self.lnkcap_l1el = 0x00038000 # l1 exit latency 
        self.lnkcap_clkpm = 0x00040000 # clock power management 
        self.lnkcap_sderc = 0x00080000 # surprise down error reporting capable 
        self.lnkcap_dlllarc = 0x00100000 # data link layer link active reporting capable 
        self.lnkcap_lbnc = 0x00200000 # link bandwidth notification capability 
        self.lnkcap_pn = 0xff000000 # port number 
        self.lnkctl = 0x10            # link control 
        self.lnkctl_aspmc = 0x0003            # aspm control 
        self.lnkctl_aspm_l0s = 0x0001            # l0s enable 
        self.lnkctl_aspm_l1 = 0x0002            # l1 enable 
        self.lnkctl_rcb = 0x0008            # read completion boundary 
        self.lnkctl_ld = 0x0010            # link disable 
        self.lnkctl_rl = 0x0020            # retrain link 
        self.lnkctl_ccc = 0x0040            # common clock configuration 
        self.lnkctl_es = 0x0080            # extended synch 
        self.lnkctl_clkreq_en = 0x0100 # enable clkreq 
        self.lnkctl_hawd = 0x0200            # hardware autonomous width disable 
        self.lnkctl_lbmie = 0x0400            # link bandwidth management interrupt enable 
        self.lnkctl_labie = 0x0800            # link autonomous bandwidth interrupt enable 
        self.lnksta = 0x12            # link status 
        self.lnksta_cls = 0x000f            # current link speed 
        self.lnksta_cls_2_5gb = 0x0001 # current link speed 2.5gt/s 
        self.lnksta_cls_5_0gb = 0x0002 # current link speed 5.0gt/s 
        self.lnksta_cls_8_0gb = 0x0003 # current link speed 8.0gt/s 
        self.lnksta_cls_16_0gb = 0x0004 # current link speed 16.0gt/s 
        self.lnksta_cls_32_0gb = 0x0005 # current link speed 32.0gt/s 
        self.lnksta_cls_64_0gb = 0x0006 # current link speed 64.0gt/s 
        self.lnksta_nlw = 0x03f0            # negotiated link width 
        self.lnksta_nlw_x1 = 0x0010            # current link width x1 
        self.lnksta_nlw_x2 = 0x0020            # current link width x2 
        self.lnksta_nlw_x4 = 0x0040            # current link width x4 
        self.lnksta_nlw_x8 = 0x0080            # current link width x8 
        self.lnksta_nlw_shift = 4            # start of nlw mask in link status 
        self.lnksta_lt = 0x0800            # link training 
        self.lnksta_slc = 0x1000            # slot clock configuration 
        self.lnksta_dllla = 0x2000            # data link layer link active 
        self.lnksta_lbms = 0x4000            # link bandwidth management status 
        self.lnksta_labs = 0x8000            # link autonomous bandwidth status 
        self.cap_exp_endpoint_sizeof_v1 = 20            # v1 endpoints with link end here 
        self.sltcap = 0x14            # slot capabilities 
        self.sltcap_abp = 0x00000001 # attention button present 
        self.sltcap_pcp = 0x00000002 # power controller present 
        self.sltcap_mrlsp = 0x00000004 # mrl sensor present 
        self.sltcap_aip = 0x00000008 # attention indicator present 
        self.sltcap_pip = 0x00000010 # power indicator present 
        self.sltcap_hps = 0x00000020 # hot-plug surprise 
        self.sltcap_hpc = 0x00000040 # hot-plug capable 
        self.sltcap_splv = 0x00007f80 # slot power limit value 
        self.sltcap_spls = 0x00018000 # slot power limit scale 
        self.sltcap_eip = 0x00020000 # electromechanical interlock present 
        self.sltcap_nccs = 0x00040000 # no command completed support 
        self.sltcap_psn = 0xfff80000 # physical slot number 
        self.sltctl = 0x18            # slot control 
        self.sltctl_abpe = 0x0001            # attention button pressed enable 
        self.sltctl_pfde = 0x0002            # power fa t detected enable 
        self.sltctl_mrlsce = 0x0004            # mrl sensor changed enable 
        self.sltctl_pdce = 0x0008            # presence detect changed enable 
        self.sltctl_ccie = 0x0010            # command completed interrupt enable 
        self.sltctl_hpie = 0x0020            # hot-plug interrupt enable 
        self.sltctl_aic = 0x00c0            # attention indicator control 
        self.sltctl_attn_ind_shift = 6      # attention indicator shift 
        self.sltctl_attn_ind_on = 0x0040 # attention indicator on 
        self.sltctl_attn_ind_blink = 0x0080 # attention indicator blinking 
        self.sltctl_attn_ind_off = 0x00c0 # attention indicator off 
        self.sltctl_pic = 0x0300            # power indicator control 
        self.sltctl_pwr_ind_on = 0x0100 # power indicator on 
        self.sltctl_pwr_ind_blink = 0x0200 # power indicator blinking 
        self.sltctl_pwr_ind_off = 0x0300 # power indicator off 
        self.sltctl_pcc = 0x0400            # power controller control 
        self.sltctl_pwr_on = 0x0000 # power on 
        self.sltctl_pwr_off = 0x0400 # power off 
        self.sltctl_eic = 0x0800            # electromechanical interlock control 
        self.sltctl_dllsce = 0x1000            # data link layer state changed enable 
        self.sltctl_aspl_disable = 0x2000 # auto slot power limit disable 
        self.sltctl_ibpd_disable = 0x4000 # in-band pd disable 
        self.sltsta = 0x1a            # slot status 
        self.sltsta_abp = 0x0001            # attention button pressed 
        self.sltsta_pfd = 0x0002            # power fa t detected 
        self.sltsta_mrlsc = 0x0004            # mrl sensor changed 
        self.sltsta_pdc = 0x0008            # presence detect changed 
        self.sltsta_cc = 0x0010            # command completed 
        self.sltsta_mrlss = 0x0020            # mrl sensor state 
        self.sltsta_pds = 0x0040            # presence detect state 
        self.sltsta_eis = 0x0080            # electromechanical interlock status 
        self.sltsta_dllsc = 0x0100            # data link layer state changed 
        self.rtctl = 0x1c            # root control 
        self.rtctl_secee = 0x0001            # system error on correctable error 
        self.rtctl_senfee = 0x0002            # system error on non-fatal error 
        self.rtctl_sefee = 0x0004            # system error on fatal error 
        self.rtctl_pmeie = 0x0008            # pme interrupt enable 
        self.rtctl_crssve = 0x0010            # crs software visibility enable 
        self.rtcap = 0x1e            # root capabilities 
        self.rtcap_crsvis = 0x0001            # crs software visibility capability 
        self.rtsta = 0x20            # root status 
        self.rtsta_pme_rq_id = 0x0000ffff # pme requester id 
        self.rtsta_pme = 0x00010000 # pme status 
        self.rtsta_pending = 0x00020000 # pme pending 
        # the device capabilities 2, device status 2, device control 2,
        # link capabilities 2, link status 2, link control 2,
        # slot capabilities 2, slot status 2, and slot control 2 registers
        # are only present on devices with pcie capability version 2.
        self.devcap2 = 0x24            # device capabilities 2 
        self.devcap2_comp_tmout_dis = 0x00000010 # completion timeout disable supported 
        self.devcap2_ari = 0x00000020 # alternative routing-id 
        self.devcap2_atomic_route = 0x00000040 # atomic op routing 
        self.devcap2_atomic_comp32 = 0x00000080 # 32b atomicop completion 
        self.devcap2_atomic_comp64 = 0x00000100 # 64b atomicop completion 
        self.devcap2_atomic_comp128 = 0x00000200 # 128b atomicop completion 
        self.devcap2_ltr = 0x00000800 # latency tolerance reporting 
        self.devcap2_obff_mask = 0x000c0000 # obff support mechanism 
        self.devcap2_obff_msg = 0x00040000 # new message signaling 
        self.devcap2_obff_wake = 0x00080000 # re-use wake#  for obff 
        self.devcap2_ee_prefix = 0x00200000 # end-end tlp prefix 
        self.devctl2 = 0x28            # device control 2 
        self.devctl2_comp_timeout = 0x000f            # completion timeout value 
        self.devctl2_comp_tmout_dis = 0x0010            # completion timeout disable 
        self.devctl2_ari = 0x0020            # alternative routing-id 
        self.devctl2_atomic_req = 0x0040            # set atomic requests 
        self.devctl2_atomic_egress_block = 0x0080 # block atomic egress 
        self.devctl2_ido_req_en = 0x0100            # allow ido for requests 
        self.devctl2_ido_cmp_en = 0x0200            # allow ido for completions 
        self.devctl2_ltr_en = 0x0400            # enable ltr mechanism 
        self.devctl2_obff_msga_en = 0x2000            # enable obff message type a 
        self.devctl2_obff_msgb_en = 0x4000            # enable obff message type b 
        self.devctl2_obff_wake_en = 0x6000            # obff using wake#  signaling 
        self.devsta2 = 0x2a            # device status 2 
        self.cap_exp_rc_endpoint_sizeof_v2 = 0x2c            # end of v2 eps w/o link 
        self.lnkcap2 = 0x2c            # link capabilities 2 
        self.lnkcap2_sls_2_5gb = 0x00000002 # supported speed 2.5gt/s 
        self.lnkcap2_sls_5_0gb = 0x00000004 # supported speed 5gt/s 
        self.lnkcap2_sls_8_0gb = 0x00000008 # supported speed 8gt/s 
        self.lnkcap2_sls_16_0gb = 0x00000010 # supported speed 16gt/s 
        self.lnkcap2_sls_32_0gb = 0x00000020 # supported speed 32gt/s 
        self.lnkcap2_sls_64_0gb = 0x00000040 # supported speed 64gt/s 
        self.lnkcap2_crosslink = 0x00000100 # crosslink supported 
        self.lnkctl2 = 0x30            # link control 2 
        self.lnkctl2_tls = 0x000f
        self.lnkctl2_tls_2_5gt = 0x0001 # supported speed 2.5gt/s 
        self.lnkctl2_tls_5_0gt = 0x0002 # supported speed 5gt/s 
        self.lnkctl2_tls_8_0gt = 0x0003 # supported speed 8gt/s 
        self.lnkctl2_tls_16_0gt = 0x0004 # supported speed 16gt/s 
        self.lnkctl2_tls_32_0gt = 0x0005 # supported speed 32gt/s 
        self.lnkctl2_tls_64_0gt = 0x0006 # supported speed 64gt/s 
        self.lnkctl2_enter_comp = 0x0010 # enter compliance 
        self.lnkctl2_tx_margin = 0x0380 # transmit margin 
        self.lnkctl2_hasd = 0x0020 # hw autonomous speed disable 
        self.lnksta2 = 0x32            # link status 2 
        self.lnksta2_flit = 0x0400 # flit mode status 
        self.cap_exp_endpoint_sizeof_v2 = 0x32            # end of v2 eps w/ link 
        self.sltcap2 = 0x34            # slot capabilities 2 
        self.sltcap2_ibpd = 0x00000001 # in-band pd disable supported 
        self.sltctl2 = 0x38            # slot control 2 
        self.sltsta2 = 0x3a            # slot status 2 

class pcie_ext_aer(object):
    def __init__(self):
        
        # advanced error reporting 
        self.id = 0x1
        self.base_addr = 0
        self.err_uncor_status = 0x04            # uncorrectable error status 
        self.err_unc_und = 0x00000001            # undefined 
        self.err_unc_dlp = 0x00000010            # data link protocol 
        self.err_unc_surpdn = 0x00000020            # surprise down 
        self.err_unc_poison_tlp = 0x00001000            # poisoned tlp 
        self.err_unc_fcp = 0x00002000            # flow control protocol 
        self.err_unc_comp_time = 0x00004000            # completion timeout 
        self.err_unc_comp_abort = 0x00008000            # completer abort 
        self.err_unc_unx_comp = 0x00010000            # unexpected completion 
        self.err_unc_rx_over = 0x00020000            # receiver overflow 
        self.err_unc_malf_tlp = 0x00040000            # malformed tlp 
        self.err_unc_ecrc = 0x00080000            # ecrc error status 
        self.err_unc_unsup = 0x00100000            # unsupported request 
        self.err_unc_acsv = 0x00200000            # acs violation 
        self.err_unc_intn = 0x00400000            # internal error 
        self.err_unc_mcbtlp = 0x00800000            # mc blocked tlp 
        self.err_unc_atomeg = 0x01000000            # atomic egress blocked 
        self.err_unc_tlppre = 0x02000000            # tlp prefix blocked 
        self.err_uncor_mask = 0x08            # uncorrectable error mask 
        # same bits as above 
        self.err_uncor_sever = 0x0c            # uncorrectable error severity 
                    # same bits as above 
        self.err_cor_status = 0x10            # correctable error status 
        self.err_cor_rcvr = 0x00000001            # receiver error status 
        self.err_cor_bad_tlp = 0x00000040            # bad tlp status 
        self.err_cor_bad_dllp = 0x00000080            # bad dllp status 
        self.err_cor_rep_roll = 0x00000100            # replay_num rollover 
        self.err_cor_rep_timer = 0x00001000            # replay timer timeout 
        self.err_cor_adv_nfat = 0x00002000            # advisory non-fatal 
        self.err_cor_internal = 0x00004000            # corrected internal 
        self.err_cor_log_over = 0x00008000            # header log overflow 
        self.err_cor_mask = 0x14            # correctable error mask 
                    # same bits as above 
        self.err_cap = 0x18            # advanced error capabilities & ctrl
        #self.err_cap_fep(x) = ((x) & 0x1f)            # first error pointer 
        self.err_cap_ecrc_genc = 0x00000020            # ecrc generation capable 
        self.err_cap_ecrc_gene = 0x00000040            # ecrc generation enable 
        self.err_cap_ecrc_chkc = 0x00000080            # ecrc check capable 
        self.err_cap_ecrc_chke = 0x00000100            # ecrc check enable 
        self.err_header_log = 0x1c            # header log register (16 bytes) 
        self.err_root_command = 0x2c            # root error command 
        self.err_root_cmd_cor_en = 0x00000001 # correctable err reporting enable 
        self.err_root_cmd_nonfatal_en = 0x00000002 # non-fatal err reporting enable 
        self.err_root_cmd_fatal_en = 0x00000004 # fatal err reporting enable 
        self.err_root_status = 0x30
        self.err_root_cor_rcv = 0x00000001 # err_cor received 
        self.err_root_mti_cor_rcv = 0x00000002 # m tiple err_cor 
        self.err_root_uncor_rcv = 0x00000004 # err_fatal/nonfatal 
        self.err_root_mti_uncor_rcv = 0x00000008 # m tiple fatal/nonfatal 
        self.err_root_first_fatal = 0x00000010 # first unc is fatal 
        self.err_root_nonfatal_rcv = 0x00000020 # non-fatal received 
        self.err_root_fatal_rcv = 0x00000040 # fatal received 
        self.err_root_aer_irq = 0xf8000000 # advanced error interrupt message number 
        self.err_root_err_src = 0x34            # error source identification 

class pcie_ext_aspm(object):

    def __init__(self):
        
        # aspm l1 pm substates 
        self.id           =  0x1e
        self.base_addr    =  0x0       # get live data
        self.l1ss_cap = 0x04            # capabilities register 
        self.l1ss_cap_pcipm_l1_2 = 0x00000001  # pci-pm l1.2 supported 
        self.l1ss_cap_pcipm_l1_1 = 0x00000002  # pci-pm l1.1 supported 
        self.l1ss_cap_aspm_l1_2 = 0x00000004  # aspm l1.2 supported 
        self.l1ss_cap_aspm_l1_1 = 0x00000008  # aspm l1.1 supported 
        self.l1ss_cap_l1_pm_ss = 0x00000010  # l1 pm substates supported 
        self.l1ss_cap_cm_restore_time = 0x0000ff00  # port common_mode_restore_time 
        self.l1ss_cap_p_pwr_on_scale = 0x00030000  # port t_power_on scale 
        self.l1ss_cap_p_pwr_on_value = 0x00f80000  # port t_power_on value 
        self.l1ss_ctl1 = 0x08            # control 1 register 
        self.l1ss_ctl1_pcipm_l1_2 = 0x00000001  # pci-pm l1.2 enable 
        self.l1ss_ctl1_pcipm_l1_1 = 0x00000002  # pci-pm l1.1 enable 
        self.l1ss_ctl1_aspm_l1_2 = 0x00000004  # aspm l1.2 enable 
        self.l1ss_ctl1_aspm_l1_1 = 0x00000008  # aspm l1.1 enable 
        self.l1ss_ctl1_l1_2_mask = 0x00000005
        self.l1ss_ctl1_l1ss_mask = 0x0000000f
        self.l1ss_ctl1_cm_restore_time = 0x0000ff00  # common_mode_restore_time 
        self.l1ss_ctl1_ltr_l12_th_value = 0x03ff0000  # ltr_l1.2_threshold_value 
        self.l1ss_ctl1_ltr_l12_th_scale = 0xe0000000  # ltr_l1.2_threshold_scale 
        self.l1ss_ctl2 = 0x0c            # control 2 register 
        self.l1ss_ctl2_t_pwr_on_scale = 0x00000003  # t_power_on scale 
        self.l1ss_ctl2_t_pwr_on_value = 0x000000f8  # t_power_on value 

class pcie_ext_ptm(object):
    def __init__(self):        
        # precision time measurement 
        self.id = 0x1f
        self.base_addr = 0
        self.ptm_cap_id = 0x1f
        self.ptm_cap    = 0x04    # ptm capability 
        self.ptm_cap_req = 0x00000001  # requester capable 
        self.ptm_cap_res = 0x00000002  # responder capable 
        self.ptm_cap_root = 0x00000004  # root capable 
        self.ptm_granarity_mask = 0x0000ff00  # clock gran arity 
        self.ptm_ctrl = 0x08    # ptm control 
        self.ptm_ctrl_enable = 0x00000001  # ptm enable 
        self.ptm_ctrl_root = 0x00000002  # root select
