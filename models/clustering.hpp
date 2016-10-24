// Code generated by Stan version 2.9

#include <stan/model/model_header.hpp>

namespace clustering_model_namespace {

using std::istream;
using std::string;
using std::stringstream;
using std::vector;
using stan::io::dump;
using stan::math::lgamma;
using stan::model::prob_grad;
using namespace stan::math;

typedef Eigen::Matrix<double,Eigen::Dynamic,1> vector_d;
typedef Eigen::Matrix<double,1,Eigen::Dynamic> row_vector_d;
typedef Eigen::Matrix<double,Eigen::Dynamic,Eigen::Dynamic> matrix_d;

static int current_statement_begin__;
class clustering_model : public prob_grad {
private:
    int N;
    int D;
    int K;
    double mu_std;
    double sigma_mean;
    double sigma_std;
    vector<vector_d> y;
    vector_d ones;
public:
    clustering_model(stan::io::var_context& context__,
        std::ostream* pstream__ = 0)
        : prob_grad(0) {
        current_statement_begin__ = -1;

        static const char* function__ = "clustering_model_namespace::clustering_model";
        (void) function__; // dummy call to supress warning
        size_t pos__;
        (void) pos__; // dummy call to supress warning
        std::vector<int> vals_i__;
        std::vector<double> vals_r__;
        context__.validate_dims("data initialization", "N", "int", context__.to_vec());
        N = int(0);
        vals_i__ = context__.vals_i("N");
        pos__ = 0;
        N = vals_i__[pos__++];
        context__.validate_dims("data initialization", "D", "int", context__.to_vec());
        D = int(0);
        vals_i__ = context__.vals_i("D");
        pos__ = 0;
        D = vals_i__[pos__++];
        context__.validate_dims("data initialization", "K", "int", context__.to_vec());
        K = int(0);
        vals_i__ = context__.vals_i("K");
        pos__ = 0;
        K = vals_i__[pos__++];
        context__.validate_dims("data initialization", "mu_std", "double", context__.to_vec());
        mu_std = double(0);
        vals_r__ = context__.vals_r("mu_std");
        pos__ = 0;
        mu_std = vals_r__[pos__++];
        context__.validate_dims("data initialization", "sigma_mean", "double", context__.to_vec());
        sigma_mean = double(0);
        vals_r__ = context__.vals_r("sigma_mean");
        pos__ = 0;
        sigma_mean = vals_r__[pos__++];
        context__.validate_dims("data initialization", "sigma_std", "double", context__.to_vec());
        sigma_std = double(0);
        vals_r__ = context__.vals_r("sigma_std");
        pos__ = 0;
        sigma_std = vals_r__[pos__++];
        validate_non_negative_index("y", "N", N);
        validate_non_negative_index("y", "D", D);
        y = std::vector<vector_d>(N,vector_d(D));
        context__.validate_dims("data initialization", "y", "vector_d", context__.to_vec(N,D));
        vals_r__ = context__.vals_r("y");
        pos__ = 0;
        size_t y_i_vec_lim__ = D;
        for (size_t i_vec__ = 0; i_vec__ < y_i_vec_lim__; ++i_vec__) {
            size_t y_limit_0__ = N;
            for (size_t i_0__ = 0; i_0__ < y_limit_0__; ++i_0__) {
                y[i_0__][i_vec__] = vals_r__[pos__++];
            }
        }

        // validate data
        check_greater_or_equal(function__,"N",N,0);
        check_greater_or_equal(function__,"D",D,0);
        check_greater_or_equal(function__,"K",K,0);
        check_greater_or_equal(function__,"mu_std",mu_std,0);
        check_greater_or_equal(function__,"sigma_mean",sigma_mean,0);
        check_greater_or_equal(function__,"sigma_std",sigma_std,0);
        validate_non_negative_index("ones", "K", K);
        ones = vector_d(K);

        double DUMMY_VAR__(std::numeric_limits<double>::quiet_NaN());
        (void) DUMMY_VAR__;  // suppress unused var warning


        // initialize transformed variables to avoid seg fault on val access
        stan::math::fill(ones,DUMMY_VAR__);

        try {
            current_statement_begin__ = 13;
            for (int k = 1; k <= K; ++k) {
                current_statement_begin__ = 14;
                stan::math::assign(get_base1_lhs(ones,k,"ones",1), 1);
            }
        } catch (const std::exception& e) {
            stan::lang::rethrow_located(e,current_statement_begin__);
            // Next line prevents compiler griping about no return
throw std::runtime_error("*** IF YOU SEE THIS, PLEASE REPORT A BUG ***");
        }

        // validate transformed data

        // set parameter ranges
        num_params_r__ = 0U;
        param_ranges_i__.clear();
        num_params_r__ += D * K;
        ++num_params_r__;
        num_params_r__ += (K - 1);
    }

    ~clustering_model() { }


    void transform_inits(const stan::io::var_context& context__,
                         std::vector<int>& params_i__,
                         std::vector<double>& params_r__,
                         std::ostream* pstream__) const {
        stan::io::writer<double> writer__(params_r__,params_i__);
        size_t pos__;
        (void) pos__; // dummy call to supress warning
        std::vector<double> vals_r__;
        std::vector<int> vals_i__;

        if (!(context__.contains_r("mu")))
            throw std::runtime_error("variable mu missing");
        vals_r__ = context__.vals_r("mu");
        pos__ = 0U;
        context__.validate_dims("initialization", "mu", "vector_d", context__.to_vec(K,D));
        std::vector<vector_d> mu(K,vector_d(D));
        for (int j1__ = 0U; j1__ < D; ++j1__)
            for (int i0__ = 0U; i0__ < K; ++i0__)
                mu[i0__](j1__) = vals_r__[pos__++];
        for (int i0__ = 0U; i0__ < K; ++i0__)
            try {
            writer__.vector_unconstrain(mu[i0__]);
        } catch (const std::exception& e) { 
            throw std::runtime_error(std::string("Error transforming variable mu: ") + e.what());
        }

        if (!(context__.contains_r("sigma")))
            throw std::runtime_error("variable sigma missing");
        vals_r__ = context__.vals_r("sigma");
        pos__ = 0U;
        context__.validate_dims("initialization", "sigma", "double", context__.to_vec());
        double sigma(0);
        sigma = vals_r__[pos__++];
        try {
            writer__.scalar_lb_unconstrain(0,sigma);
        } catch (const std::exception& e) { 
            throw std::runtime_error(std::string("Error transforming variable sigma: ") + e.what());
        }

        if (!(context__.contains_r("pi")))
            throw std::runtime_error("variable pi missing");
        vals_r__ = context__.vals_r("pi");
        pos__ = 0U;
        context__.validate_dims("initialization", "pi", "vector_d", context__.to_vec(K));
        vector_d pi(K);
        for (int j1__ = 0U; j1__ < K; ++j1__)
            pi(j1__) = vals_r__[pos__++];
        try {
            writer__.simplex_unconstrain(pi);
        } catch (const std::exception& e) { 
            throw std::runtime_error(std::string("Error transforming variable pi: ") + e.what());
        }

        params_r__ = writer__.data_r();
        params_i__ = writer__.data_i();
    }

    void transform_inits(const stan::io::var_context& context,
                         Eigen::Matrix<double,Eigen::Dynamic,1>& params_r,
                         std::ostream* pstream__) const {
      std::vector<double> params_r_vec;
      std::vector<int> params_i_vec;
      transform_inits(context, params_i_vec, params_r_vec, pstream__);
      params_r.resize(params_r_vec.size());
      for (int i = 0; i < params_r.size(); ++i)
        params_r(i) = params_r_vec[i];
    }


    template <bool propto__, bool jacobian__, typename T__>
    T__ log_prob(vector<T__>& params_r__,
                 vector<int>& params_i__,
                 std::ostream* pstream__ = 0) const {

        T__ DUMMY_VAR__(std::numeric_limits<double>::quiet_NaN());
        (void) DUMMY_VAR__;  // suppress unused var warning

        T__ lp__(0.0);
        stan::math::accumulator<T__> lp_accum_params__;
        stan::math::accumulator<T__> lp_accum_data__;

        // model parameters
        stan::io::reader<T__> in__(params_r__,params_i__);

        vector<Eigen::Matrix<T__,Eigen::Dynamic,1> > mu;
        size_t dim_mu_0__ = K;
        mu.reserve(dim_mu_0__);
        for (size_t k_0__ = 0; k_0__ < dim_mu_0__; ++k_0__) {
            if (jacobian__)
                mu.push_back(in__.vector_constrain(D,lp__));
            else
                mu.push_back(in__.vector_constrain(D));
        }

        T__ sigma;
        (void) sigma;   // dummy to suppress unused var warning
        if (jacobian__)
            sigma = in__.scalar_lb_constrain(0,lp__);
        else
            sigma = in__.scalar_lb_constrain(0);

        Eigen::Matrix<T__,Eigen::Dynamic,1>  pi;
        (void) pi;   // dummy to suppress unused var warning
        if (jacobian__)
            pi = in__.simplex_constrain(K,lp__);
        else
            pi = in__.simplex_constrain(K);


        // transformed parameters
        vector<vector<T__> > z(N, (vector<T__>(K)));

        // initialize transformed variables to avoid seg fault on val access
        stan::math::fill(z,DUMMY_VAR__);

        try {
            current_statement_begin__ = 25;
            for (int n = 1; n <= N; ++n) {
                current_statement_begin__ = 26;
                for (int k = 1; k <= K; ++k) {
                    current_statement_begin__ = 27;
                    stan::math::assign(get_base1_lhs(get_base1_lhs(z,n,"z",1),k,"z",2), ((log(get_base1(pi,k,"pi",1)) - (D * log(sigma))) - (0.5 * (dot_self(subtract(get_base1(mu,k,"mu",1),get_base1(y,n,"y",1))) / (sigma * sigma)))));
                }
            }
        } catch (const std::exception& e) {
            stan::lang::rethrow_located(e,current_statement_begin__);
            // Next line prevents compiler griping about no return
throw std::runtime_error("*** IF YOU SEE THIS, PLEASE REPORT A BUG ***");
        }

        // validate transformed parameters
        for (int i0__ = 0; i0__ < N; ++i0__) {
            for (int i1__ = 0; i1__ < K; ++i1__) {
                if (stan::math::is_uninitialized(z[i0__][i1__])) {
                    std::stringstream msg__;
                    msg__ << "Undefined transformed parameter: z" << '[' << i0__ << ']' << '[' << i1__ << ']';
                    throw std::runtime_error(msg__.str());
                }
            }
        }

        const char* function__ = "validate transformed params";
        (void) function__; // dummy to suppress unused var warning

        // model body
        try {
            current_statement_begin__ = 32;
            for (int k = 1; k <= K; ++k) {
                current_statement_begin__ = 33;
                for (int d = 1; d <= D; ++d) {
                    current_statement_begin__ = 34;
                    lp_accum_params__.add(normal_log<propto__>(get_base1(get_base1(mu,k,"mu",1),d,"mu",2), 0, mu_std));
                }
            }
            current_statement_begin__ = 35;
            lp_accum_params__.add(normal_log<propto__>(sigma, sigma_mean, sigma_std));
            current_statement_begin__ = 36;
            lp_accum_params__.add(dirichlet_log<propto__>(pi, ones));
            current_statement_begin__ = 39;
            for (int n = 1; n <= N; ++n) {
                current_statement_begin__ = 40;
                lp_accum_data__.add(log_sum_exp(get_base1(z,n,"z",1)));
            }
        } catch (const std::exception& e) {
            stan::lang::rethrow_located(e,current_statement_begin__);
            // Next line prevents compiler griping about no return
throw std::runtime_error("*** IF YOU SEE THIS, PLEASE REPORT A BUG ***");
        }

        lp_accum_params__.add(lp__);
        return lp_accum_params__.sum() + alpha__ * lp_accum_data__.sum();

    } // log_prob()

    template <bool propto, bool jacobian, typename T_>
    T_ log_prob(Eigen::Matrix<T_,Eigen::Dynamic,1>& params_r,
               std::ostream* pstream = 0) const {
      std::vector<T_> vec_params_r;
      vec_params_r.reserve(params_r.size());
      for (int i = 0; i < params_r.size(); ++i)
        vec_params_r.push_back(params_r(i));
      std::vector<int> vec_params_i;
      return log_prob<propto,jacobian,T_>(vec_params_r, vec_params_i, pstream);
    }


    template <typename RNG>
    void exact_sample(RNG& base_rng__,
                      std::vector<double>& vars_param__,
                      std::vector<double>& vars_data_r__,
                      std::vector<int>& vars_data_i__) {


        // declare model parameters
        vector<vector_d> mu(K, (vector_d(D)));
        double sigma(0.0);
        (void) sigma;  // dummy to suppress unused var warning
        vector_d pi(K);
        (void) pi;  // dummy to suppress unused var warning

        double DUMMY_VAR__(std::numeric_limits<double>::quiet_NaN());
        (void) DUMMY_VAR__;  // suppress unused var warning
        // initialize transformed variables to avoid seg fault on val access
        stan::math::fill(mu,DUMMY_VAR__);
        stan::math::fill(sigma,DUMMY_VAR__);
        stan::math::fill(pi,DUMMY_VAR__);


        // model body
        try {
            current_statement_begin__ = 32;
            for (int k = 1; k <= K; ++k) {
                current_statement_begin__ = 33;
                for (int d = 1; d <= D; ++d) {
                    current_statement_begin__ = 34;
                    stan::math::assign(get_base1_lhs(get_base1_lhs(mu,k,"mu",1),d,"mu",2), normal_rng(0, mu_std, base_rng__));
                }
            }
            current_statement_begin__ = 35;
            stan::math::assign(sigma, normal_rng(sigma_mean, sigma_std, base_rng__));
            current_statement_begin__ = 36;
            stan::math::assign(pi, dirichlet_rng(ones, base_rng__));
            current_statement_begin__ = 39;
            // for (int n = 1; n <= N; ++n) {
            //     current_statement_begin__ = 40;
            //     lp_accum__.add(log_sum_exp(get_base1(z,n,"z",1)));
            // }
        } catch (const std::exception& e) {
            stan::lang::rethrow_located(e,current_statement_begin__);
            // Next line prevents compiler griping about no return
throw std::runtime_error("*** IF YOU SEE THIS, PLEASE REPORT A BUG ***");
        }

        // write parameter vars
        for (int k_1__ = 0; k_1__ < D; ++k_1__) {
            for (int k_0__ = 0; k_0__ < K; ++k_0__) {
                vars_param__.push_back(mu[k_0__][k_1__]);
            }
        }
        vars_param__.push_back(sigma);
        for (int k_0__ = 0; k_0__ < K; ++k_0__) {
            vars_param__.push_back(pi[k_0__]);
        }

        // write data vars
        vars_data_i__.push_back(N);
        vars_data_i__.push_back(D);
        vars_data_i__.push_back(K);
        vars_data_r__.push_back(mu_std);
        vars_data_r__.push_back(sigma_mean);
        vars_data_r__.push_back(sigma_std);
        for (int k_1__ = 0; k_1__ < D; ++k_1__) {
            for (int k_0__ = 0; k_0__ < N; ++k_0__) {
                vars_data_r__.push_back(y[k_0__][k_1__]);
            }
        }

    }


    void get_param_names(std::vector<std::string>& names__) const {
        names__.resize(0);
        names__.push_back("mu");
        names__.push_back("sigma");
        names__.push_back("pi");
        // names__.push_back("z");
    }


    void get_data_r_names(std::vector<std::string>& names__) const {
        names__.resize(0);
        names__.push_back("mu_std");
        names__.push_back("sigma_mean");
        names__.push_back("sigma_std");
        names__.push_back("y");
    }


    void get_data_i_names(std::vector<std::string>& names__) const {
        names__.resize(0);
        names__.push_back("N");
        names__.push_back("D");
        names__.push_back("K");
    }


    void get_dims(std::vector<std::vector<size_t> >& dimss__) const {
        dimss__.resize(0);
        std::vector<size_t> dims__;
        dims__.resize(0);
        dims__.push_back(K);
        dims__.push_back(D);
        dimss__.push_back(dims__);
        dims__.resize(0);
        dimss__.push_back(dims__);
        dims__.resize(0);
        dims__.push_back(K);
        dimss__.push_back(dims__);
        dims__.resize(0);
        dims__.push_back(N);
        dims__.push_back(K);
        dimss__.push_back(dims__);
    }


    void get_param_dims(std::vector<std::vector<size_t> >& dimss__) const {
        dimss__.resize(0);
        std::vector<size_t> dims__;
        dims__.resize(0);
        dims__.push_back(K);
        dims__.push_back(D);
        dimss__.push_back(dims__);
        dims__.resize(0);
        dimss__.push_back(dims__);
        dims__.resize(0);
        dims__.push_back(K);
        dimss__.push_back(dims__);
    }


    void get_data_r_dims(std::vector<std::vector<size_t> >& dimss__) const {
        dimss__.resize(0);
        std::vector<size_t> dims__;
        dims__.resize(0);
        dimss__.push_back(dims__);
        dims__.resize(0);
        dimss__.push_back(dims__);
        dims__.resize(0);
        dimss__.push_back(dims__);
        dims__.resize(0);
        dims__.push_back(N);
        dims__.push_back(D);
        dimss__.push_back(dims__);
    }


    void get_data_i_dims(std::vector<std::vector<size_t> >& dimss__) const {
        dimss__.resize(0);
        std::vector<size_t> dims__;
        dims__.resize(0);
        dimss__.push_back(dims__);
        dims__.resize(0);
        dimss__.push_back(dims__);
        dims__.resize(0);
        dimss__.push_back(dims__);
    }

    template <typename RNG>
    void write_array(RNG& base_rng__,
                     std::vector<double>& params_r__,
                     std::vector<int>& params_i__,
                     std::vector<double>& vars__,
                     bool include_tparams__ = true,
                     bool include_gqs__ = true,
                     std::ostream* pstream__ = 0) const {
        vars__.resize(0);
        stan::io::reader<double> in__(params_r__,params_i__);
        static const char* function__ = "clustering_model_namespace::write_array";
        (void) function__; // dummy call to supress warning
        // read-transform, write parameters
        vector<vector_d> mu;
        size_t dim_mu_0__ = K;
        for (size_t k_0__ = 0; k_0__ < dim_mu_0__; ++k_0__) {
            mu.push_back(in__.vector_constrain(D));
        }
        double sigma = in__.scalar_lb_constrain(0);
        vector_d pi = in__.simplex_constrain(K);
        for (int k_1__ = 0; k_1__ < D; ++k_1__) {
            for (int k_0__ = 0; k_0__ < K; ++k_0__) {
                vars__.push_back(mu[k_0__][k_1__]);
            }
        }
        vars__.push_back(sigma);
        for (int k_0__ = 0; k_0__ < K; ++k_0__) {
            vars__.push_back(pi[k_0__]);
        }

        if (!include_tparams__) return;
        // declare and define transformed parameters
        double lp__ = 0.0;
        (void) lp__; // dummy call to supress warning
        stan::math::accumulator<double> lp_accum__;

        vector<vector<double> > z(N, (vector<double>(K, 0.0)));

        try {
            current_statement_begin__ = 25;
            for (int n = 1; n <= N; ++n) {
                current_statement_begin__ = 26;
                for (int k = 1; k <= K; ++k) {
                    current_statement_begin__ = 27;
                    stan::math::assign(get_base1_lhs(get_base1_lhs(z,n,"z",1),k,"z",2), ((log(get_base1(pi,k,"pi",1)) - (D * log(sigma))) - (0.5 * (dot_self(subtract(get_base1(mu,k,"mu",1),get_base1(y,n,"y",1))) / (sigma * sigma)))));
                }
            }
        } catch (const std::exception& e) {
            stan::lang::rethrow_located(e,current_statement_begin__);
            // Next line prevents compiler griping about no return
throw std::runtime_error("*** IF YOU SEE THIS, PLEASE REPORT A BUG ***");
        }

        // validate transformed parameters

        // write transformed parameters
        for (int k_1__ = 0; k_1__ < K; ++k_1__) {
            for (int k_0__ = 0; k_0__ < N; ++k_0__) {
                vars__.push_back(z[k_0__][k_1__]);
            }
        }

        if (!include_gqs__) return;
        // declare and define generated quantities

        double DUMMY_VAR__(std::numeric_limits<double>::quiet_NaN());
        (void) DUMMY_VAR__;  // suppress unused var warning


        // initialize transformed variables to avoid seg fault on val access

        try {
        } catch (const std::exception& e) {
            stan::lang::rethrow_located(e,current_statement_begin__);
            // Next line prevents compiler griping about no return
throw std::runtime_error("*** IF YOU SEE THIS, PLEASE REPORT A BUG ***");
        }

        // validate generated quantities

        // write generated quantities
    }

    template <typename RNG>
    void write_array(RNG& base_rng,
                     Eigen::Matrix<double,Eigen::Dynamic,1>& params_r,
                     Eigen::Matrix<double,Eigen::Dynamic,1>& vars,
                     bool include_tparams = true,
                     bool include_gqs = true,
                     std::ostream* pstream = 0) const {
      std::vector<double> params_r_vec(params_r.size());
      for (int i = 0; i < params_r.size(); ++i)
        params_r_vec[i] = params_r(i);
      std::vector<double> vars_vec;
      std::vector<int> params_i_vec;
      write_array(base_rng,params_r_vec,params_i_vec,vars_vec,include_tparams,include_gqs,pstream);
      vars.resize(vars_vec.size());
      for (int i = 0; i < vars.size(); ++i)
        vars(i) = vars_vec[i];
    }

    static std::string model_name() {
        return "clustering_model";
    }


    void constrained_param_names(std::vector<std::string>& param_names__,
                                 bool include_tparams__ = true,
                                 bool include_gqs__ = true) const {
        std::stringstream param_name_stream__;
        for (int k_1__ = 1; k_1__ <= D; ++k_1__) {
            for (int k_0__ = 1; k_0__ <= K; ++k_0__) {
                param_name_stream__.str(std::string());
                param_name_stream__ << "mu" << '.' << k_0__ << '.' << k_1__;
                param_names__.push_back(param_name_stream__.str());
            }
        }
        param_name_stream__.str(std::string());
        param_name_stream__ << "sigma";
        param_names__.push_back(param_name_stream__.str());
        for (int k_0__ = 1; k_0__ <= K; ++k_0__) {
            param_name_stream__.str(std::string());
            param_name_stream__ << "pi" << '.' << k_0__;
            param_names__.push_back(param_name_stream__.str());
        }

        if (!include_gqs__ && !include_tparams__) return;
        for (int k_1__ = 1; k_1__ <= K; ++k_1__) {
            for (int k_0__ = 1; k_0__ <= N; ++k_0__) {
                param_name_stream__.str(std::string());
                param_name_stream__ << "z" << '.' << k_0__ << '.' << k_1__;
                param_names__.push_back(param_name_stream__.str());
            }
        }

        if (!include_gqs__) return;
    }


    void unconstrained_param_names(std::vector<std::string>& param_names__,
                                   bool include_tparams__ = true,
                                   bool include_gqs__ = true) const {
        std::stringstream param_name_stream__;
        for (int k_1__ = 1; k_1__ <= D; ++k_1__) {
            for (int k_0__ = 1; k_0__ <= K; ++k_0__) {
                param_name_stream__.str(std::string());
                param_name_stream__ << "mu" << '.' << k_0__ << '.' << k_1__;
                param_names__.push_back(param_name_stream__.str());
            }
        }
        param_name_stream__.str(std::string());
        param_name_stream__ << "sigma";
        param_names__.push_back(param_name_stream__.str());
        for (int k_0__ = 1; k_0__ <= (K - 1); ++k_0__) {
            param_name_stream__.str(std::string());
            param_name_stream__ << "pi" << '.' << k_0__;
            param_names__.push_back(param_name_stream__.str());
        }

        if (!include_gqs__ && !include_tparams__) return;
        for (int k_1__ = 1; k_1__ <= K; ++k_1__) {
            for (int k_0__ = 1; k_0__ <= N; ++k_0__) {
                param_name_stream__.str(std::string());
                param_name_stream__ << "z" << '.' << k_0__ << '.' << k_1__;
                param_names__.push_back(param_name_stream__.str());
            }
        }

        if (!include_gqs__) return;
    }

}; // model

} // namespace

typedef clustering_model_namespace::clustering_model stan_model;

