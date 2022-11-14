require 'socket'
sock = UDPSocket.new

sock.bind('0.0.0.0', 12345)
sock.connect('8.8.8.8', 53)

def make_question_header(query_id)
  # id, flags, num questions, num answers, num auth, num additional
  [query_id, 0x0100, 0x0001, 0x0000, 0x0000, 0x0000].pack('nnnnnn')
end

def encode_domain_name(domain)
  domain
    .split(".")
    .map { |x| x.length.chr + x }
    .join + "\0"
end

def make_dns_query(domain, type)
  query_id = rand(65535)
  header = make_question_header(query_id)
  question =  encode_domain_name(domain) + [type, 1].pack('nn')
  print question
  header + question
end

query_id = rand(65535)
header = make_question_header(query_id)
print ["b96201000001000000000000"].pack("H*")

sock.send(make_dns_query("example.com", 1), 0)
reply, _ = sock.recvfrom(1024)
puts reply.unpack('H*')
