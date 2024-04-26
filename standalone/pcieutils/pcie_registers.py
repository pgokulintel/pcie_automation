class devcap(object):
    def __init__(self, value):
        self.devcap   = 0x04           # device capabilities
        self.payload  = (value & 0x00000007)  # max_payload_size 
        self.phantom  = (value & 0x00000018) >> 3 # phantom functions 
        self.ext_tag  = (value & 0x00000020) >> 5 # extended tags 
        self.l0s      = (value & 0x000001c0) >> 6 # l0s acceptable latency 
        self.l1       = (value & 0x00000e00) >> 9 # l1 acceptable latency 
        self.rber     = (value & 0x00008000) >> 15 # role-based error reporting 
        self.pwr_val  = (value & 0x03fc0000) >> 18 # slot power limit value 
        self.pwr_scl  = (value & 0x0c000000) >> 26 # slot power limit scale 
        self.flr      = (value & 0x10000000) >> 28 # function level reset 

class devcntl(object):
    def __init__(self, value = 0):
        self.devctl         = 0x08                    # device control 
        self.cere           = (value & 0x0001)        # correctable error reporting en.
        self.nfere          = (value & 0x0002) >> 1   # non-fatal error reporting enable 
        self.fere           = (value & 0x0004) >> 2   # fatal error reporting enable 
        self.urre           = (value & 0x0008) >> 3   # unsupported request reporting en. 
        self.relax_en       = (value & 0x0010) >> 4   # enable relaxed ordering 
        self.payload        = (value & 0x00e0) >> 5   # max_payload_size 
        self.ext_tag        = (value & 0x0100) >> 8   # extended tag field enable 
        self.phantom        = (value & 0x0200) >> 9   # phantom functions enable 
        self.aux_pme        = (value & 0x0400) >> 10  # auxiliary power pm enable 
        self.nosnoop_en     = (value & 0x0800) >> 11  # enable no snoop 
        self.readrq         = (value & 0x7000) >> 12  # max_read_request_size 
        self.devctl_bcr_flr = (value & 0x8000) >> 15  # bridge configuration retry / flr 

class devsts(object):
    def __init__(self, value = 0):
        self.devsta       = 0x0a                   # device status 
        self.ced          = (value & 0x0001)       # correctable error detected 
        self.nfed         = (value & 0x0002) >> 1  # non-fatal error detected 
        self.fed          = (value & 0x0004) >> 2  # fatal error detected 
        self.urd          = (value & 0x0008) >> 3  # unsupported request detected 
        self.auxpd        = (value & 0x0010) >> 4  # aux power detected 
        self.trpnd        = (value & 0x0020) >> 5  # transactions pending 

class linkcap(object):
    def __init__(self, value):
        self.lnkcap         = 0x0c                       # link capabilities 
        self.sls     = (value & 0x0000000f)       # supported link speeds 
        self.mlw     = (value & 0x000003f0) >> 4  # maximum link width 
        self.aspms   = (value & 0x00000c00) >> 10 # aspm support
        self.aspm_l0s = self.aspms & 1
        self.aspm_l1  = (self.aspms & 2) >> 1
        self.l0sel   = (value & 0x00007000) >> 12 # l0s exit latency 
        self.l1el    = (value & 0x00038000) >> 15 # l1 exit latency 
        self.clkpm   = (value & 0x00040000) >> 18 # clock power management 
        self.sderc   = (value & 0x00080000) >> 19 # surprise down error reporting capable 
        self.dlllarc = (value & 0x00100000) >> 20 # data link layer link active reporting capable 
        self.lbnc    = (value & 0x00200000) >> 21 # link bandwidth notification capability 
        self.pn      = (value & 0xff000000) >> 24 # port number 

class linkcntl(object):
    def __init__(self, value):
        self.lnkctl           = 0x10                    # link control 
        self.aspmc     = (value & 0x0003)        # aspm control 
        self.aspm_l0s  = self.aspmc & 1
        self.aspm_l1   = (self.aspmc & 2) >> 1
        self.rcb       = (value & 0x0008) >> 3   # read completion boundary 
        self.ld        = (value & 0x0010) >> 4   # link disable 
        self.rl        = (value & 0x0020) >> 5   # retrain link 
        self.ccc       = (value & 0x0040) >> 6   # common clock configuration 
        self.es        = (value & 0x0080) >> 7   # extended synch 
        self.clkreq_en = (value & 0x0100) >> 8   # enable clkreq 
        self.hawd      = (value & 0x0200) >> 9   # hardware autonomous width disable 
        self.lbmie     = (value & 0x0400) >> 10  # link bandwidth management interrupt enable 
        self.labie     = (value & 0x0800) >> 11  # link autonomous bandwidth interrupt enable 

class linksts(object):
    def __init__(self, value):
        self.linksts = 0x12                     # link status 
        self.cls     = (value & 0x000f)         # current link speed 
        self.nlw     = (value & 0x03f0) >> 4    # negotiated link width 
        self.lt      = (value & 0x0800) >> 11   # link training 
        self.slc     = (value & 0x1000) >> 12   # slot clock configuration 
        self.dllla   = (value & 0x2000) >> 13   # data link layer link active 
        self.lbms    = (value & 0x4000) >> 14   # link bandwidth management status 
        self.labs    = (value & 0x8000) >> 15   # link autonomous bandwidth status 

class l1sscap(object):
    def __init__(self, value = 0):
        self.l1ss_cap        = 0x04                       # capabilities register 
        self.pcipm_l1_2      = (value & 0x00000001)       # pci-pm l1.2 supported 
        self.pcipm_l1_1      = (value & 0x00000002) >> 1  # pci-pm l1.1 supported 
        self.aspm_l1_2       = (value & 0x00000004) >> 2  # aspm l1.2 supported 
        self.aspm_l1_1       = (value & 0x00000008) >> 3  # aspm l1.1 supported 
        self.l1_pm_ss        = (value & 0x00000010) >> 4  # l1 pm substates supported 
        self.cm_restore_time = (value & 0x0000ff00) >> 8  # port common_mode_restore_time 
        self.p_pwr_on_scale  = (value & 0x00030000) >> 16 # port t_power_on scale 
        self.p_pwr_on_value  = (value & 0x00f80000) >> 19 # port t_power_on value 

class l1sscntl1(object):
    def __init__(self, value = 0):
        self.l1ss_ctl1        = 0x08                       # control 1 register 
        self.pcipm_l1_2       = (value & 0x00000001)       # pci-pm l1.2 enable 
        self.pcipm_l1_1       = (value & 0x00000002) >> 1  # pci-pm l1.1 enable 
        self.aspm_l1_2        = (value & 0x00000004) >> 2  # aspm l1.2 enable 
        self.aspm_l1_1        = (value & 0x00000008) >> 3  # aspm l1.1 enable 
        self.cm_restore_time  = (value & 0x0000ff00) >> 8  # common_mode_restore_time 
        self.ltr_l12_th_value = (value & 0x03ff0000) >> 12 # ltr_l1.2_threshold_value 
        self.ltr_l12_th_scale = (value & 0xe0000000) >> 28 # ltr_l1.2_threshold_scale 

class l1sscntl2(object):
    def __init__(self, value = 0):
        self.l1ss_ctl2      = 0x0c                       # control 2 register 
        self.t_pwr_on_scale = (value & 0x00000003)       # t_power_on scale 
        self.t_pwr_on_value = (value & 0x000000f8) >> 3  # t_power_on value 

class pciecap(object):
    def __init__(self, value = 0):
        # pci express capability registers 
        self.id                            = 0x10
        self.offset                        = 0x0
        self.std_cap = 1
        self.pcie_cap                     = 0x02           # capabilities register 
        self.pcie_cap_vers            = 0x000f         # capability version 
        self.pcie_cap_type            = 0x00f0         # device/port type 
        self.pcie_cap_slot                  = 0x0100         # slot implemented 
        self.pcie_cap_flags_irq             = 0x3e00         # interrupt message number 
        self.cap_exp_rc_endpoint_sizeof_v1 = 12            # v1 endpoints without link end here 
        self.cap_exp_endpoint_sizeof_v1 = 20            # v1 endpoints with link end here 

class sltcap(object):
    def __init__(self, value = 0):
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

class sltcntl(object):
    def __init__(self, value = 0):
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

class sltsts(object):
    def __init__(self, value = 0):
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

class rootcntl(object):
    def __init__(self, value = 0):
        self.rtctl = 0x1c            # root control 
        self.rtctl_secee = 0x0001            # system error on correctable error 
        self.rtctl_senfee = 0x0002            # system error on non-fatal error 
        self.rtctl_sefee = 0x0004            # system error on fatal error 
        self.rtctl_pmeie = 0x0008            # pme interrupt enable 
        self.rtctl_crssve = 0x0010            # crs software visibility enable 

class rootcap(object):
    def __init__(self, value = 0):
        self.rtcap = 0x1e            # root capabilities 
        self.rtcap_crsvis = 0x0001            # crs software visibility capability 

class rootsts(object):
    def __init__(self, value = 0):
        self.rtsta = 0x20            # root status 
        self.rtsta_pme_rq_id = 0x0000ffff # pme requester id 
        self.rtsta_pme = 0x00010000 # pme status 
        self.rtsta_pending = 0x00020000 # pme pending 
        # the device capabilities 2, device status 2, device control 2,
        # link capabilities 2, link status 2, link control 2,
        # slot capabilities 2, slot status 2, and slot control 2 registers
        # are only present on devices with pcie capability version 2.

class devcap2(object):
    def __init__(self, value = 0):
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


class devcntl2(object):
    def __init__(self, value = 0):
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

class devsts2(object):
    def __init__(self, value = 0):
        self.devsta2 = 0x2a            # device status 2 
        self.cap_exp_rc_endpoint_sizeof_v2 = 0x2c            # end of v2 eps w/o link 

class linkcap2(object):
    def __init__(self, value = 0):
        self.lnkcap2 = 0x2c            # link capabilities 2 
        self.lnkcap2_sls_2_5gb = 0x00000002 # supported speed 2.5gt/s 
        self.lnkcap2_sls_5_0gb = 0x00000004 # supported speed 5gt/s 
        self.lnkcap2_sls_8_0gb = 0x00000008 # supported speed 8gt/s 
        self.lnkcap2_sls_16_0gb = 0x00000010 # supported speed 16gt/s 
        self.lnkcap2_sls_32_0gb = 0x00000020 # supported speed 32gt/s 
        self.lnkcap2_sls_64_0gb = 0x00000040 # supported speed 64gt/s 
        self.lnkcap2_crosslink = 0x00000100 # crosslink supported 

class linkcntl2(object):
    def __init__(self, value = 0):
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

class linksts2(object):
    def __init__(self, value = 0):
        self.lnksta2 = 0x32            # link status 2 
        self.lnksta2_flit = 0x0400 # flit mode status 
        self.cap_exp_endpoint_sizeof_v2 = 0x32            # end of v2 eps w/ link 

class sltcap2(object):
    def __init__(self, value = 0):
        self.sltcap2 = 0x34            # slot capabilities 2 
        self.sltcap2_ibpd = 0x00000001 # in-band pd disable supported 

class sltctl2(object):
    def __init__(self, value = 0):
        self.sltctl2 = 0x38            # slot control 2 

class sltsta2(object):
    def __init__(self, value = 0):
        self.sltsta2 = 0x3a            # slot status 2 