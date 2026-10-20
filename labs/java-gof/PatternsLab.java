import java.util.*;
import java.util.function.Consumer;

/** Independent GoF examples, no vendor runtime. JDK 17 required. */
public final class PatternsLab {
  record Request(String id, int amount, String role) {}
  record Decision(boolean approved, String reason) {}
  interface Policy { Decision evaluate(Request r); }
  static final class LimitStrategy implements Policy {
    private final int limit;
    LimitStrategy(int limit) { this.limit=limit; }
    public Decision evaluate(Request r) { return new Decision(r.amount()<=limit, r.amount()<=limit ? "OK":"LIMIT"); }
  }
  static final class PolicyFactory {
    Policy create(String profile) {
      return switch(profile) {
        case "strict" -> new LimitStrategy(1000);
        case "normal" -> new LimitStrategy(5000);
        default -> throw new IllegalArgumentException("Unknown profile");
      };
    }
  }
  interface Command { Decision execute(); }
  record Evaluate(Policy policy, Request request) implements Command {
    public Decision execute() { return policy.evaluate(request); }
  }
  static final class AuditDecorator implements Policy {
    private final Policy target; private final List<Decision> audit;
    AuditDecorator(Policy target,List<Decision> audit) { this.target=target; this.audit=audit; }
    public Decision evaluate(Request r) { Decision d=target.evaluate(r); audit.add(d); return d; }
  }
  static final class ProtectionProxy implements Policy {
    private final Policy target;
    ProtectionProxy(Policy target) { this.target=target; }
    public Decision evaluate(Request r) {
      if (!"decision-reader".equals(r.role())) throw new SecurityException("Forbidden");
      return target.evaluate(r);
    }
  }
  static abstract class Workflow {
    final Decision execute(Request r) {
      if(r==null || r.id()==null || r.id().isBlank() || r.amount()<0) throw new IllegalArgumentException();
      return perform(r);
    }
    protected abstract Decision perform(Request r);
  }
  static final class NormalWorkflow extends Workflow {
    private final Policy policy;
    NormalWorkflow(Policy p) { policy=p; }
    protected Decision perform(Request r) { return policy.evaluate(r); }
  }
  static final class DecisionEvents {
    private final List<Consumer<Decision>> subscribers=new ArrayList<>();
    void subscribe(Consumer<Decision> c) { subscribers.add(c); }
    void publish(Decision d) { for(var s:subscribers) s.accept(d); }
  }
  private static void ok(boolean b) { if(!b) throw new AssertionError(); }
  public static void main(String[] args) {
    PolicyFactory factory=new PolicyFactory();
    Request request=new Request("R-1",2000,"decision-reader");
    ok(!factory.create("strict").evaluate(request).approved()); // Strategy
    boolean failed=false;
    try {factory.create("unlisted");} catch(IllegalArgumentException e) {failed=true;}
    ok(failed); // Factory fail closed
    var audit=new ArrayList<Decision>();
    Policy policy=new ProtectionProxy(new AuditDecorator(factory.create("normal"),audit));
    ok(new Evaluate(policy,request).execute().approved()); // Command
    ok(audit.size()==1); // Decorator
    failed=false;
    try {policy.evaluate(new Request("R-2",100,"guest"));} catch(SecurityException e){failed=true;}
    ok(failed && audit.size()==1); // Proxy fail closed
    var workflow=new NormalWorkflow(factory.create("strict"));
    failed=false;
    try {workflow.execute(new Request("",-1,"decision-reader"));}catch(IllegalArgumentException e){failed=true;}
    ok(failed && !workflow.execute(request).approved()); // Template Method
    var events=new DecisionEvents(); var seen=new ArrayList<String>();
    events.subscribe(d->seen.add("audit")); events.subscribe(d->seen.add("metrics"));
    events.publish(new Decision(true,"OK"));
    ok(seen.equals(List.of("audit","metrics"))); // Observer
    System.out.println("GOF_LAB_PASS=7/7");
  }
}
