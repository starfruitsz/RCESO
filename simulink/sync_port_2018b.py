# sync_port_2018b.py —— 由 simulink/ 的权威版本生成 R2018b 移植包，并校验一致性
# 用法：
#   python sync_port_2018b.py          # 生成/更新 port_2018b/
#   python sync_port_2018b.py --check  # 只校验，不写文件；不一致则非零退出
import hashlib, io, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.join(HERE, 'port_2018b')
FILES = ['b0_ident_m.m', 'build_foc_m.m', 'run_foc_m.m', 'test_b0_m.m',
         'README_2018b.md', '移植步骤_R2018b.md']

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()[:16]

def main():
    check = '--check' in sys.argv
    os.makedirs(PKG, exist_ok=True)
    bad = []
    print('%-18s %-18s %s' % ('文件', '源 sha256[:16]', '包内状态'))
    for name in FILES:
        src = os.path.join(HERE, name)
        dst = os.path.join(PKG, name)
        s = sha(src)
        if check:
            ok = os.path.exists(dst) and sha(dst) == s
            print('%-18s %-18s %s' % (name, s, 'OK' if ok else '不一致'))
            if not ok:
                bad.append(name)
        else:
            shutil.copyfile(src, dst)
            print('%-18s %-18s %s' % (name, s, '已同步'))
    if check and bad:
        print('\n不一致：' + ', '.join(bad) + '（跑 python sync_port_2018b.py 同步）')
        sys.exit(1)
    if check:
        print('\n包与源一致。')
    else:
        print('\n包已更新：%s' % PKG)

if __name__ == '__main__':
    main()
