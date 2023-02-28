from utils import *
import os
import sys

root_domain = os.getenv('ROOT').replace(".onion","")
resolved = resolveDomain(root_domain)
if resolved:
	print(f"ROOT domain {root_domain}.onion already exists as {resolved}.onion")
	sys.exit(0)

print(f"ROOT domain {root_domain}.onion is not in database")
unreal = createDomains([root_domain])
print(f"Created as {unreal[0]}.onion")
