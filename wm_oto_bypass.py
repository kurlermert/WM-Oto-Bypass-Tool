import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class VMXEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("ipcontrolpanel.com WM OTO BYPASS")
        self.root.geometry("600x780")
        self.root.configure(bg="#2C2F33")

        
        def get_icon_path():
            if getattr(sys, 'frozen', False):
                return os.path.join(sys._MEIPASS, "wmware.ico")
            return "wmware.ico"

        self.root.iconbitmap(get_icon_path())

        title_label = tk.Label(root, text="ipcontrolpanel.com WM OTO BYPASS", font=("Arial", 14, "bold"), fg="white", bg="#23272A", pady=10)
        title_label.pack(fill="x")

        self.checkbuttons = []
        self.var_list = []

        self.btn_select_dir = tk.Button(root, text="📂 VMware Dizin Seç", font=("Arial", 12), bg="#5865F2", fg="white", width=40, height=2, command=self.select_directory)
        self.btn_select_dir.pack(pady=10)

        self.frame = tk.Frame(root, bg="#2C2F33")
        self.frame.pack(expand=True, fill="both", padx=10, pady=5)

        self.canvas = tk.Canvas(self.frame, bg="#2C2F33")
        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg="#2C2F33")

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set, width=550, height=250)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.btn_process = tk.Button(root, text="✅ Seçilenleri İşle", font=("Arial", 12), bg="#57F287", fg="black", width=40, height=2, command=self.process_selection)
        self.btn_process.pack(pady=10)

        self.label_result = tk.Label(root, text="", font=("Arial", 11), fg="white", bg="#2C2F33")
        self.label_result.pack(pady=5)

        footer_frame = tk.Frame(root, bg="#23272A", height=40)
        footer_frame.pack(fill="x", side="bottom")

        self.signature_label = tk.Label(footer_frame, text="by aksamci", font=("Arial", 10, "italic"), fg="lightgray", bg="#23272A")
        self.signature_label.pack(pady=5)

    def list_vms(self, vmware_dir):
        vms = []
        for root, dirs, files in os.walk(vmware_dir):
            for file in files:
                if file.endswith(".vmx"):
                    vms.append(os.path.join(root, file))
        return vms

    def append_to_vmx(self, vmx_path):
        try:
            with open(vmx_path, "r") as file:
                content = file.read()
            
            fixed_code = """
hypervisor.cpuid.v0 = "FALSE"
board-id.reflectHost = "TRUE"
hw.model.reflectHost = "TRUE"
serialNumber.reflectHost = "TRUE"
smbios.reflectHost = "TRUE"
SMBIOS.noOEMStrings = "TRUE"
isolation.tools.getPtrLocation.disable = "TRUE"
isolation.tools.setPtrLocation.disable = "TRUE"
isolation.tools.setVersion.disable = "TRUE"
isolation.tools.getVersion.disable = "TRUE"
monitor_control.disable_directexec = "TRUE"
monitor_control.disable_chksimd = "TRUE"
monitor_control.disable_ntreloc = "TRUE"
monitor_control.disable_selfmod = "TRUE"
monitor_control.disable_reloc = "TRUE"
monitor_control.disable_btinout = "TRUE"
monitor_control.disable_btmemspace = "TRUE"
monitor_control.disable_btpriv = "TRUE"
monitor_control.disable_btseg = "TRUE"
monitor_control.restrict_backdoor = "TRUE"
scsi0:0.productID = ""
scsi0:0.vendorID = ""
""".strip()

            if fixed_code in content:
                return f"⚠️ Zaten eklenmiş: {os.path.basename(vmx_path)}"

            with open(vmx_path, "a") as file:
                file.write("\n" + fixed_code)
            
            return f"✅ Güncellendi: {os.path.basename(vmx_path)}"
        except Exception as e:
            return f"❌ Hata ({os.path.basename(vmx_path)}): {e}"

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            vm_paths = self.list_vms(directory)
            self.display_vms(vm_paths)

    def display_vms(self, vm_paths):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        self.checkbuttons.clear()
        self.var_list.clear()

        if not vm_paths:
            messagebox.showinfo("Bilgi", "📁 Seçilen dizinde VMX dosyası bulunamadı.")
            return

        for vm in vm_paths:
            var = tk.BooleanVar()
            chk = tk.Checkbutton(self.scroll_frame, text=os.path.basename(vm), variable=var, font=("Arial", 11), anchor="w", bg="#2C2F33", fg="white", selectcolor="#40444B")
            chk.vmx_path = vm
            chk.pack(anchor="w", pady=3, padx=10, fill="x")
            
            self.var_list.append(var)
            self.checkbuttons.append(chk)

    def process_selection(self):
        selected_vmx_files = [chk.vmx_path for chk, var in zip(self.checkbuttons, self.var_list) if var.get()]

        if not selected_vmx_files:
            messagebox.showwarning("⚠️ Uyarı", "Lütfen en az bir VMX dosyası seçin.")
            return

        results = []
        
        for vmx_path in selected_vmx_files:
            result = self.append_to_vmx(vmx_path)
            results.append(result)
        
        messagebox.showinfo("✔️ İşlem Tamamlandı", "\n".join(results))
        self.label_result.config(text="📌 İşlem tamamlandı. Detaylar için bilgi kutusuna bakın.", fg="#57F287")

root = tk.Tk()
app = VMXEditor(root)
root.mainloop()
